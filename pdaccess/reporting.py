"""Paired analysis of NEW runs, kept separate from the recorded paper reanalysis."""
import csv
import json
from pathlib import Path
from .core import DIMS, seed_for
from .analyze_recovered import bh


def write_csv(path, rows):
    if not rows:
        return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)


def load_runs(paths):
    records=[];seen=set();cohort=None;kind=None
    for path in map(Path,paths):
        meta=json.loads((path/'run.json').read_text())
        if cohort is None:cohort=meta['manifest_sha256'];kind=meta['artifact_kind']
        if cohort!=meta['manifest_sha256'] or kind!=meta['artifact_kind']:
            raise ValueError('Do not mix different cohorts or synthetic/actual runs')
        rows=[json.loads(line) for line in (path/'results.jsonl').read_text().splitlines() if line.strip()]
        expected=meta['recorded_results']*len(meta['methods'])
        if len(rows)!=expected:raise ValueError(f'Incomplete run: {path}: {len(rows)} / {expected}')
        per_person={}
        for row in rows:
            key=(row['target'],row['persona_id'],row['method'])
            if key in seen:raise ValueError(f'Duplicate target/persona/method: {key}')
            if row['artifact_kind']!=kind:raise ValueError('Result provenance differs from run metadata')
            seen.add(key);per_person.setdefault(row['persona_id'],[]).append(row)
        if len(per_person)!=meta['recorded_results']:raise ValueError('Incorrect persona count')
        for bundle in per_person.values():
            if {r['method'] for r in bundle}!=set(meta['methods']):raise ValueError('Incomplete method pairing')
            first=[json.dumps({'first':r['history'][0],'gold':r['gold'],'calls':r['shared_first_call_ids']},sort_keys=True) for r in bundle]
            if len(set(first))!=1:raise ValueError('Paired methods must share gold and exact first question/answer/calls')
        records.extend(rows)
    if not records:raise ValueError('No records')
    return records,kind


def paired_effect(a,b,seed,repetitions=10000):
    import numpy as np
    from scipy.stats import wilcoxon
    delta=np.asarray(b,dtype=float)-np.asarray(a,dtype=float)
    if not len(delta) or not np.isfinite(delta).all():raise ValueError('Invalid paired values')
    nonzero=delta!=0
    statistic,p=(0.,1.) if not nonzero.any() else wilcoxon(delta,zero_method='wilcox',correction=False,alternative='two-sided',method='auto')
    rng=np.random.default_rng(seed)
    means=[]
    for start in range(0,repetitions,256):
        indices=rng.integers(0,len(delta),size=(min(256,repetitions-start),len(delta)))
        means.extend(delta[indices].mean(axis=1))
    ci=np.percentile(means,[2.5,97.5])
    return {'n':len(delta),'n_nonzero':int(nonzero.sum()),'difference':float(delta.mean()),'ci_low':float(ci[0]),'ci_high':float(ci[1]),
            'wilcoxon_W':float(statistic),'p_raw':float(p),'positive':int((delta>0).sum()),'negative':int((delta<0).sum()),'ties':int((delta==0).sum())}


def analyze_runs(paths,output,repetitions=10000):
    import numpy as np
    from scipy.stats import binomtest
    if repetitions<100:raise ValueError('Use at least 100 bootstrap replicates')
    records,kind=load_runs(paths)
    dest=Path(output)
    if dest.exists():raise FileExistsError(dest)
    dest.mkdir(parents=True)
    by_cell={}
    for row in records:by_cell.setdefault((row['target'],row['method']),{})[row['persona_id']]=row
    metrics=[];comparisons=[];dimensions=[];diagnostics=[]
    for (target,method),mapping in sorted(by_cell.items()):
        rs=list(mapping.values());ags=[r['scoring']['average_gain'] for r in rs]
        item={'target':target,'method':method,'n':len(rs),'average_gain':float(np.mean(ags)) if all(v is not None for v in ags) else None,
              'mean_turns':float(np.mean([r['turns'] for r in rs])), 'early_stop_rate':float(np.mean([r['turns']<5 for r in rs]))}
        item.update({d+'_accuracy':float(np.mean([r['scoring']['correct'][d] for r in rs])) for d in DIMS})
        for key in ('input_tokens','output_tokens'):
            vals=[r[key] for r in rs];item['mean_'+key]=float(np.mean(vals)) if all(v is not None for v in vals) else None
        metrics.append(item)
        if method=='selective':
            decisions=[d for r in rs for d in r['decisions']]
            diagnostics.append({'target':target,'decisions':len(decisions),'gate_activation_rate':sum(bool(d.get('gate_active')) for d in decisions)/len(decisions) if decisions else None,
                'graph_selection_rate':sum(bool(d.get('selected_graph')) for d in decisions)/len(decisions) if decisions else None,'early_stop_rate':item['early_stop_rate']})
    families={'original':'primary_original_vs_adaptive','online':'graph_diagnostics','selective':'graph_diagnostics',
              'random_candidate':'expanded_controls','round_robin':'expanded_controls','dialogue':'expanded_controls','generic':'expanded_controls',
              'direct':'controller_ablations','no_coverage':'controller_ablations','no_redundancy':'controller_ablations','uncertainty':'active_uncertainty'}
    for target in sorted({t for t,m in by_cell}):
        adaptive=by_cell.get((target,'adaptive'))
        if adaptive is None:continue
        for method,family in families.items():
            other=by_cell.get((target,method))
            if other is None:continue
            if set(adaptive)!=set(other):raise ValueError('Different persona IDs across paired conditions')
            ids=sorted(adaptive)
            a=[other[i]['scoring']['average_gain'] for i in ids];b=[adaptive[i]['scoring']['average_gain'] for i in ids]
            if any(v is None for v in a+b):continue
            comparisons.append({'target':target,'comparison':'adaptive - '+method,'family':family,**paired_effect(a,b,seed_for(target,method,'bootstrap'),repetitions)})
            if method=='original':
                for dim in DIMS:
                    aa=np.array([other[i]['scoring']['correct'][dim] for i in ids]);bb=np.array([adaptive[i]['scoring']['correct'][dim] for i in ids])
                    loss=int(((aa==1)&(bb==0)).sum());gain=int(((aa==0)&(bb==1)).sum())
                    dimensions.append({'target':target,'dimension':dim,'original_only_correct':loss,'adaptive_only_correct':gain,'accuracy_difference':float((bb-aa).mean()),'p_raw':float(binomtest(loss,loss+gain,.5).pvalue) if loss+gain else 1.})
    for family in set(r['family'] for r in comparisons):
        group=[r for r in comparisons if r['family']==family]
        for row,p in zip(group,bh([r['p_raw'] for r in group])):row['p_bh']=p
    for row,p in zip(dimensions,bh([r['p_raw'] for r in dimensions])):row['p_bh']=p
    for row in diagnostics:
        online=next((x for x in metrics if x['target']==row['target'] and x['method']=='online'),None)
        selective=next(x for x in metrics if x['target']==row['target'] and x['method']=='selective')
        row['input_token_reduction_vs_online']=1-selective['mean_input_tokens']/online['mean_input_tokens'] if online and online['mean_input_tokens'] and selective['mean_input_tokens'] is not None else None
    report={'artifact_kind':kind,'historical_results':False,'bootstrap_repetitions':repetitions,'metrics':metrics,'paired_tests':comparisons,'dimension_tests':dimensions,'selective_diagnostics':diagnostics,
            'notes':['Synthetic runs are plumbing checks, never model evidence.','BH correction is separate per named comparison family; missing target models change the family size.','Token counts are logical per-method attribution, including shared initial calls; missing usage remains null.','Undefined gain (baseline=1) produces null and no paired AG test.']}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    for name,rows in [('method_metrics',metrics),('paired_tests',comparisons),('dimension_tests',dimensions),('selective_diagnostics',diagnostics)]:write_csv(dest/(name+'.csv'),rows)
    return report
