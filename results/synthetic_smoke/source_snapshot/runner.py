"""Paired execution with exact request/response cache and explicit reconstruction provenance."""
import copy
import json
import math
import platform
import random
import sys
from collections import Counter
from pathlib import Path
from . import __version__
from . import prompts
from .backend import Backend
from .core import (DIMS, Graph, ROOT, Schema, clamp, digest, gate, last_object,
                   majority_baselines, score_prediction, seed_for, selective_stop, validate_manifest)

METHODS=('original','adaptive','online','selective','random_candidate','round_robin',
         'dialogue','generic','direct','no_coverage','no_redundancy','uncertainty')
PRIMARY=('original','adaptive','online','selective')


def source_fingerprint():
    paths=list((ROOT/'pdaccess').glob('*.py'))+list((ROOT/'config').glob('*.json'))
    return digest({str(p.relative_to(ROOT)):p.read_text() for p in sorted(paths)})


def run(manifest, config, output, methods=PRIMARY, mock=False, resume=False, limit=None):
    schema=Schema()
    rows=validate_manifest(manifest,schema)
    if limit is not None:
        if limit<1:
            raise ValueError('limit must be positive')
        rows=rows[:limit]
    if not methods or len(set(methods))!=len(methods) or any(m not in METHODS for m in methods):
        raise ValueError('Unknown, duplicate or empty methods')
    if config.get('budget') != 5:
        raise ValueError('This reconstruction fixes the manuscript five-question budget')
    if any(not config[x].get('revision') for x in ('agent','target')):
        raise ValueError('Checkpoint revisions must be recorded')
    output=Path(output)
    run_spec={'version':__version__,'config':config,'manifest_sha256':digest(manifest),
              'source_sha256':source_fingerprint(),'methods':list(methods),'mock':mock,'limit':limit}
    fingerprint=digest(run_spec)
    if output.exists():
        if not resume:
            raise FileExistsError('Output exists. Use a fresh path or --resume.')
        old=json.loads((output/'run.json').read_text())
        if old['fingerprint']!=fingerprint:
            raise ValueError('Resume refused: code/config/manifest/methods differ')
    else:
        output.mkdir(parents=True)
        metadata={**run_spec,'fingerprint':fingerprint,'python':sys.version,'platform':platform.platform(),
                  'artifact_kind':'synthetic_smoke_only' if mock else 'new_reconstruction_experiment',
                  'historical_results':False,'server_revision_verification':'not verified by HTTP protocol',
                  'recorded_results':len(rows),'majority_cohort_size':len(manifest['personas'])}
        (output/'run.json').write_text(json.dumps(metadata,indent=2))
        (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
        (output/'prompt_snapshot.json').write_text(json.dumps({'systems':prompts.SYSTEM,'fallback':prompts.FALLBACK,
             'forbidden':prompts.FORBIDDEN,'recorded_examples':prompts.RECORDED,'provenance':'mixed: recovered dialogue-role wording and observed fallback bank; reconstructed Online/Selective wording and runtime serializers'},ensure_ascii=False,indent=2))
        # Preserve exact reconstruction code for later inspection, without copying any .env or old repository.
        for p in (ROOT/'pdaccess').glob('*.py'):
            dest=output/'source_snapshot'/p.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(p.read_bytes())
    backend=Backend(config,output,mock)
    baselines=majority_baselines(manifest['personas'])
    results_path=output/'results.jsonl'
    records=[json.loads(x) for x in results_path.read_text().splitlines()] if results_path.exists() else []
    completed={(r['persona_id'],r['method']) for r in records}
    for row in rows:
        if all((row['id'],m) in completed for m in methods):
            continue
        ident=row['id']; persona=row['persona']; base=config['base_seed']; target=config['target']['model']
        context={'persona_id':ident,'method':'shared','turn':1}
        q,qid=backend.complete('initial',prompts.messages('initial',{}),seed_for(base,target,ident,'initial'),context=context)
        q=prompts.clean_choice({'selected_question':q},1,schema)['question']
        answer,aid=backend.complete('target',prompts.target_messages(persona,[],q),seed_for(base,target,ident,'target',1,'shared'),target=True,context=context)
        shared_ids=[qid,aid]
        for method in methods:
            if (ident,method) in completed:
                continue
            graph=Graph(); history=[{'question':q,'answer':answer}]; decisions=[]; asked=Counter()
            call_ids=shared_ids[:]
            def call(role,payload,turn,sample=0):
                text,cid=backend.complete(role,prompts.messages(role,payload),
                    seed_for(base,target,ident,'adaptive' if method=='random_candidate' and role=='adaptive' else method,turn,role,sample),
                    context={'persona_id':ident,'method':method,'turn':turn,'sample':sample})
                call_ids.append(cid)
                return text
            for turn in range(1,config['budget']+1):
                payload={'CURRENT_RESPONSE':history[-1]['answer'],'question':history[-1]['question'],
                         'earlier_dialogue':history[:-1],'previous_graph':graph.payload()}
                raw=call('integrated' if method=='selective' else 'extract',payload,turn)
                extraction=last_object(raw)
                graph.update(extraction,history[-1]['answer'])
                if turn==config['budget']:
                    break
                if method=='online':
                    raw_state=call('state',{'dialogue':history,'graph':graph.payload()},turn)
                    novelties=graph.novelties[:]
                    graph.update(last_object(raw_state),'')
                    graph.novelties=novelties
                state=graph.state()
                detail={'turn':turn,'state':state if method in ('online','selective') else None}
                if method=='selective':
                    obj=last_object(call('selective_dialogue',{'dialogue':history},turn))
                    choice=prompts.clean_choice(obj,turn+1,schema)
                    active=gate(state,turn); selected_graph=False; compared=False
                    gain=clamp(obj.get('expected_gain'))
                    if active:
                        gobj=last_object(call('selective_graph',{'dialogue':history,'graph':graph.payload(),'state':state},turn))
                        gchoice=prompts.clean_choice(gobj,turn+1,schema)
                        if not gchoice['fallback']:
                            names=['dialogue','graph']
                            random.Random(seed_for(base,target,ident,method,turn,'AB')).shuffle(names)
                            qs={'dialogue':choice['question'],'graph':gchoice['question']}
                            scores=last_object(call('utility',{'dialogue':history,'A':qs[names[0]],'B':qs[names[1]]},turn))
                            if scores:
                                from .core import utility
                                vals={names[i]:utility(scores.get(k)) for i,k in enumerate(('A','B'))}
                                compared=True; gain=max(vals.values()); selected_graph=vals['graph']>=vals['dialogue']
                                detail['utility']=vals
                                if selected_graph:
                                    choice=gchoice
                            detail['AB_order']=names
                    stop=selective_stop(state,turn,selected_graph,prompts.parse_action(obj),gain)
                    detail.update(gate_active=active,selected_graph=selected_graph,utility_compared=compared,gain=gain)
                elif method in ('adaptive','random_candidate','generic','direct','no_coverage','no_redundancy'):
                    role='adaptive' if method=='random_candidate' else method
                    obj=last_object(call(role,{'dialogue':history,'dimensions':DIMS},turn))
                    if method=='random_candidate':
                        candidates=obj.get('candidates')
                        candidates=candidates if isinstance(candidates,list) else []
                        if candidates:
                            index=seed_for(base,target,ident,turn,'random-candidate')%len(candidates)
                            selected=candidates[index]
                            obj['selected_question']=selected.get('question','') if isinstance(selected,dict) else ''
                            detail['random_index']=index
                        # Empty candidate list retains the parsed selected question, as the recovered report specifies.
                    choice=prompts.clean_choice(obj,turn+1,schema)
                    stop=choice['action']=='stop' and method not in ('random_candidate','generic')
                elif method=='online':
                    obj=last_object(call('online',{'dialogue':history,'graph':graph.payload(),'state':state},turn))
                    choice=prompts.clean_choice(obj,turn+1,schema);stop=choice['action']=='stop'
                else:
                    role=method;payload={'dialogue':history}
                    if method=='round_robin':
                        payload['focus_dimension']=DIMS[(turn-1)%4]
                    elif method=='uncertainty':
                        allowed=schema.inventory(persona)
                        samples=[last_object(call('uncertainty',{'dialogue':history,'allowed_values':allowed,
                            'categories':{d:persona[d]['category'] for d in DIMS if d!='social_role'}},turn,j)) for j in range(5)]
                        entropies={}
                        for d in DIMS:
                            values=[schema.match(x.get(d,{}).get('value') if isinstance(x.get(d),dict) else x.get(d),allowed[d]) for x in samples]
                            counts=Counter(v for v in values if v is not None);n=sum(counts.values())
                            entropies[d]=-sum((v/n)*math.log(v/n) for v in counts.values())/math.log(len(allowed[d])) if n else 0.
                        payload['focus_dimension']=max(DIMS,key=lambda d:(entropies[d],-asked[d],-DIMS.index(d)));role='round_robin'
                        detail['normalized_entropies']=entropies
                    raw=call(role,payload,turn)
                    choice=prompts.clean_choice({'selected_question':raw,'target_dimension':payload.get('focus_dimension')},turn+1,schema)
                    stop=False
                asked[choice['target_dimension']]+=1
                detail.update(choice=choice,stop=stop)
                decisions.append(detail)
                if stop:
                    break
                qnext=choice['question']
                response,cid=backend.complete('target',prompts.target_messages(persona,history,qnext),
                    seed_for(base,target,ident,method,turn+1,'target'),target=True,
                    context={'persona_id':ident,'method':method,'turn':turn+1})
                call_ids.append(cid)
                history.append({'question':qnext,'answer':response})
            prediction=last_object(call('predict',{'dialogue':history,'graph':graph.payload(),
                'allowed_values':schema.inventory(persona),
                'categories':{d:persona[d]['category'] for d in DIMS if d!='social_role'}},len(history)))
            scoring=score_prediction(schema,persona,prediction,baselines)
            usage=[]
            for cid in call_ids:
                cached=json.loads((backend.cache/(cid+'.json')).read_text())
                usage.append(cached['response'].get('usage'))
            tokens_complete=all(isinstance(u,dict) and 'prompt_tokens' in u and 'completion_tokens' in u for u in usage)
            rec={'artifact_kind':'synthetic_smoke_only' if mock else 'new_reconstruction_experiment',
                 'persona_id':ident,'method':method,'target':target,'gold':persona,'history':history,
                 'shared_first_call_ids':shared_ids,'decisions':decisions,'graph':graph.payload(),
                 'rejected_graph_items':graph.rejected,'prediction':prediction,'scoring':scoring,
                 'turns':len(history),'call_ids':call_ids,'logical_calls':len(call_ids),'tokens_complete':tokens_complete,
                 'input_tokens':sum(u['prompt_tokens'] for u in usage) if tokens_complete else None,
                 'output_tokens':sum(u['completion_tokens'] for u in usage) if tokens_complete else None}
            with results_path.open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
            records.append(rec);completed.add((ident,method))
        print('Completed persona',row['index'],flush=True)
    expected={(r['id'],m) for r in rows for m in methods}
    if completed != expected:
        raise ValueError('Result identities do not match requested paired cohort')
    summaries={}
    for method in methods:
        rs=[r for r in records if r['method']==method]
        ag=[r['scoring']['average_gain'] for r in rs]
        summaries[method]={'n':len(rs),'average_gain':sum(ag)/len(ag) if all(x is not None for x in ag) else None,
             'accuracy':{d:sum(r['scoring']['correct'][d] for r in rs)/len(rs) for d in DIMS},
             'mean_turns':sum(r['turns'] for r in rs)/len(rs)}
    summary={'artifact_kind':'synthetic_smoke_only' if mock else 'new_reconstruction_experiment',
             'majority_baselines':baselines,'methods':summaries,'note':'Null AG means a baseline equals one. Mock scores are not experimental evidence.',
             'resource_accounting':'Per-method tokens are logical attribution including shared initial calls. Unique cached call IDs give physical model-call totals; cache reuse is not new generation.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary
