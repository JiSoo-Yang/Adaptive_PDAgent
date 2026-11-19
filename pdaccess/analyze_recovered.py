"""Recompute reported primary statistics from preserved per-persona analysis inputs.
No inference, no substitution of expanded-run results for primary-run results.
"""
import csv
import json
from pathlib import Path


def bh(ps):
    order=sorted(range(len(ps)),key=ps.__getitem__);out=[0.]*len(ps);last=1.
    for rank in range(len(order),0,-1):
        i=order[rank-1];last=min(last,ps[i]*len(ps)/rank);out[i]=last
    return out


def analyze(source,output):
    import numpy as np
    import scipy
    from scipy.stats import wilcoxon,binomtest
    source=Path(source);output=Path(output);
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(output)
    output.mkdir(parents=True,exist_ok=True)
    dims=('social_role','personality','background','interests')
    def read(name):
        with (source/'m1_m2_reporting'/name).open(newline='') as f:return list(csv.DictReader(f))
    primary=read('M1_M2_raw_results.csv'); reference=read('m1_primary_summary.csv')
    # Verify the reported per-dimension gain and AG against binary outcomes.
    groups={}
    for row in primary:
        if row['method']=='dialogue_only': row['method']='adaptive'
        score=float(row['raw_score']);base=float(row['majority_baseline'])
        assert score in (0.,1.)
        assert abs((score-base)/(1-base)-float(row['normalized_gain']))<1e-12
        key=(row['target_model'],row['persona_id'],row['method'])
        assert row['dimension'] not in groups.setdefault(key,{})
        groups[key][row['dimension']]=row
    values={}
    for key,ds in groups.items():
        assert set(ds)==set(dims)
        calc=sum(float(ds[d]['normalized_gain']) for d in dims)/4
        stored=float(ds[dims[0]]['average_gain'])
        assert abs(calc-stored)<1e-12
        values[key]=stored
    tests=[];dimensions=[]
    for ref in reference:
        target=ref['target_model']
        identifiers=sorted({key[1] for key in values if key[0]==target},
            key=lambda pid:int(groups[(target,pid,'original')][dims[0]]['persona_index']))
        assert len(identifiers)==304
        a=np.array([values[(target,i,'original')] for i in identifiers])
        b=np.array([values[(target,i,'adaptive')] for i in identifiers])
        delta=b-a
        result=wilcoxon(delta,zero_method='wilcox',correction=False,alternative='two-sided',method='auto')
        rng=np.random.default_rng(int(ref['bootstrap_seed']))
        idx=rng.integers(0,304,size=(int(ref['bootstrap_repetitions']),304))
        ci=np.percentile(delta[idx].mean(axis=1),[2.5,97.5])
        row={'target':target,'n':len(delta),'original':float(a.mean()),'adaptive':float(b.mean()),
             'delta':float(delta.mean()),'W':float(result.statistic),'p':float(result.pvalue),
             'ci_low':float(ci[0]),'ci_high':float(ci[1]),'positive':int((delta>0).sum()),
             'negative':int((delta<0).sum()),'ties':int((delta==0).sum()),'bootstrap_seed':int(ref['bootstrap_seed'])}
        checks={'original':'original_mean_average_gain','adaptive':'adaptive_mean_average_gain',
                'delta':'mean_difference_adaptive_minus_original','W':'wilcoxon_statistic_min_rank_sum',
                'p':'wilcoxon_p_raw','ci_low':'ci95_low','ci_high':'ci95_high',
                'positive':'positive_pairs','negative':'negative_pairs','ties':'tied_pairs'}
        row['reference_absolute_errors']={k:abs(row[k]-float(ref[v])) for k,v in checks.items()}
        tests.append(row)
        for d in dims:
            oa=np.array([float(groups[(target,i,'original')][d]['raw_score']) for i in identifiers])
            ab=np.array([float(groups[(target,i,'adaptive')][d]['raw_score']) for i in identifiers])
            loss=int(((oa==1)&(ab==0)).sum());gain=int(((oa==0)&(ab==1)).sum())
            p=binomtest(loss,loss+gain,.5).pvalue if loss+gain else 1.
            dimensions.append({'target':target,'dimension':d,'b':loss,'c':gain,'delta':float((ab-oa).mean()),'p':float(p)})
    for row,p,ref in zip(tests,bh([r['p'] for r in tests]),reference):
        row['p_bh']=p;row['reference_absolute_errors']['p_bh']=abs(p-float(ref['p_bh']))
    dimrefs={(r['target_model'],r['dimension']):r for r in read('dimension_level_tests.csv')}
    for row,p in zip(dimensions,bh([r['p'] for r in dimensions])):
        row['p_bh']=p; ref=dimrefs[(row['target'],row['dimension'])]
        row['reference_absolute_errors']={'b':abs(row['b']-int(ref['b_original_correct_adaptive_incorrect'])),
            'c':abs(row['c']-int(ref['c_original_incorrect_adaptive_correct'])),
            'p':abs(row['p']-float(ref['mcnemar_p_raw'])),'p_bh':abs(p-float(ref['p_bh']))}
    maxerr=max(v for row in tests+dimensions for v in row['reference_absolute_errors'].values())
    report={'kind':'reanalysis_of_recorded_primary_scores','inference_performed':False,
        'numpy':np.__version__,'scipy':scipy.__version__,'validated_long_rows':len(primary),
        'primary':tests,'dimension_tests':dimensions,'max_reference_error':maxerr,'matches_within_1e_10':maxerr<1e-10,
        'scope':'Binary scores and stored persona AG validated algebraically; tests recomputed from serialized historical AG. Does not rerun inference or independently restore the original label canonicalizer.'}
    (output/'primary_reanalysis.json').write_text(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');a=p.parse_args()
    r=analyze(a.source,a.output)
    print('Primary reanalysis:',r['matches_within_1e_10'],'maximum error:',r['max_reference_error'])
    for row in r['primary']:print(row['target'],row['delta'],row['p_bh'],row['ci_low'],row['ci_high'])
