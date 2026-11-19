"""Extract provenance-linked historical artifacts; never modify supplied records."""
import csv
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path
from .core import digest


def calls_in(value,path=''):
    if isinstance(value,dict):
        if isinstance(value.get('prompt_messages'),list) and 'raw_response' in value:
            yield path,value
            return
        for k,v in value.items():
            yield from calls_in(v,path+'/'+k)
    elif isinstance(value,list):
        for i,v in enumerate(value):
            yield from calls_in(v,path+'/'+str(i))


def recover(source,output):
    source=Path(source).resolve();output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    (output/'call_examples').mkdir()
    roles=Counter(); counts=Counter(); personas={}; systems={}; examples={}; files=[]
    replacements=[]; pair_first={}; scores=[]; failures=[]
    for path in sorted(source.rglob('*.jsonl')):
        if 'raw' not in path.parts:
            continue
        sha=hashlib.sha256();n=0
        with path.open('rb') as f:
            for lineno,raw in enumerate(f,1):
                sha.update(raw)
                if not raw.strip():continue
                row=json.loads(raw);n+=1
                method=row.get('method','unknown'); target=row.get('target_model','unknown')
                family=str(path.relative_to(source)).split('/raw/')[0]
                counts[(family,target,method)]+=1
                ref={'file':str(path.relative_to(source)),'line':lineno,'persona_id':row.get('persona_id'),
                     'method':method,'target':target,'base_seed':row.get('base_seed')}
                if row.get('success') is not True:
                    failures.append(ref)
                if row.get('persona_id') and row.get('ground_truth'):
                    ident=row['persona_id'];gold=row['ground_truth']
                    if ident in personas:
                        assert personas[ident]['ground_truth']==gold,('ground truth changed',ident)
                    else:
                        personas[ident]={'persona_id':ident,'persona_index':row.get('persona_index'),
                                         'ground_truth':gold,'source':ref}
                if row.get('history'):
                    key=(family,target,row.get('persona_id'),row.get('base_seed'))
                    first=row['history'][0]
                    if key in pair_first:assert pair_first[key]==first,('unpaired first response',ref)
                    else:pair_first[key]=first
                for i,t in enumerate(row.get('turn_records',[])):
                    if t.get('question_was_replaced'):
                        replacements.append({'source':ref,'turn_record':i,'question':t.get('question'),
                          'decision':t.get('decision'),'question_label_hits':t.get('question_label_hits')})
                # Deduplicate aliased question_call / decision_call dictionaries within one record.
                seen=set()
                for pointer,call in calls_in(row):
                    cid=digest(call)
                    if cid in seen:continue
                    seen.add(cid)
                    role=call.get('role','unknown');roles[(family,method,role)]+=1
                    for msg in call['prompt_messages']:
                        if msg.get('role')!='system':continue
                        text=msg['content'];key=(role,hashlib.sha256(text.encode()).hexdigest())
                        if key not in systems:systems[key]={'role':role,'sha256':key[1],'content':text,
                            'source':{**ref,'json_pointer':pointer},'observed_calls':0}
                        systems[key]['observed_calls']+=1
                    key=(family,method,role)
                    if key not in examples:
                        obj={'kind':'verbatim_recorded_call','source':{**ref,'json_pointer':pointer},'call':call}
                        name='example_'+str(len(examples)).zfill(3)+'.json'
                        (output/'call_examples'/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
                        examples[key]=name
                if row.get('dimension_scores'):
                    scores.append({'family':family,'target':target,'method':method,
                        'persona_id':row['persona_id'],'persona_index':row['persona_index'],
                        **row['dimension_scores'],'turns':row.get('turns_used'),
                        'input_tokens':row.get('total_input_tokens'),'output_tokens':row.get('total_output_tokens')})
        files.append({'file':str(path.relative_to(source)),'rows':n,'sha256':sha.hexdigest()})
        print('Recovered',str(path.relative_to(source)),n,flush=True)
    # Verify any provided source-file hashes against the supplied files (not just names).
    checks=[]
    for manifest in [source/'main/aggregate/manifest.json',source/'m1_m2_reporting/manifest.json']:
        doc=json.loads(manifest.read_text())
        for field in ('raw_files','generated_sha256'):
            for original,expected in doc.get(field,{}).items():
                prefix='results/access_revision/'
                if not original.startswith(prefix):continue
                p=source/original[len(prefix):]
                if not p.exists():continue
                h=hashlib.sha256()
                with p.open('rb') as f:
                    for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
                checks.append({'file':str(p.relative_to(source)),'expected':expected,'actual':h.hexdigest(),'match':h.hexdigest()==expected})
    (output/'historical_personas.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sorted(personas.values(),key=lambda x:x['persona_index'])))
    (output/'system_prompts.json').write_text(json.dumps(list(systems.values()),ensure_ascii=False,indent=2))
    (output/'observed_fallback_questions.json').write_text(json.dumps(replacements,ensure_ascii=False,indent=2))
    with (output/'recorded_dimension_scores.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(scores[0]));w.writeheader();w.writerows(scores)
    result={'kind':'recovery_from_supplied_logs','source_root':str(source),'raw_files':files,
            'historical_personas':len(personas),'first_turn_pairing_groups':len(pair_first),
            'record_counts':[{'family':k[0],'target':k[1],'method':k[2],'count':v} for k,v in sorted(counts.items())],
            'call_roles':[{'family':k[0],'method':k[1],'role':k[2],'count':v} for k,v in sorted(roles.items())],
            'examples':[{'family':k[0],'method':k[1],'role':k[2],'file':'call_examples/'+v} for k,v in examples.items()],
            'system_prompt_variants':len(systems),'replaced_questions':len(replacements),
            'unsuccessful_records':failures,'file_hash_checks':checks,
            'limitations':['Serialized calls are actual recorded messages, not recovered runner source code.',
                'Only fallback questions that occurred in logs are recovered; a complete bank is not implied.',
                'Primary Original/Adaptive per-instance scores are in the separate M1/M2 CSV; expanded raw logs must not replace the primary run.',
                'Original/Adaptive/controls dominate these raw files. No full primary Online/Selective call log has been established.']}
    (output/'recovery_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');a=p.parse_args()
    result=recover(a.source,a.output)
    print('Recovered personas:',result['historical_personas'],'system prompt variants:',result['system_prompt_variants'])
