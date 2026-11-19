import argparse
import json
import os
from pathlib import Path
import urllib.request
from .core import ROOT, Schema, make_manifest, import_recovered_personas
from .runner import METHODS, PRIMARY, run


def main():
    p=argparse.ArgumentParser(description='Access reconstruction and recovered-log analysis. Never writes manuscript files.')
    sub=p.add_subparsers(dest='command',required=True)
    m=sub.add_parser('manifest',help='Generate a NEW deterministic cohort, not the historical cohort')
    m.add_argument('--count',type=int,default=304);m.add_argument('--seed',type=int,default=20260802)
    m.add_argument('--exclude');m.add_argument('--output',required=True)
    im=sub.add_parser('import-cohort',help='Import historical persona values from recovered gold records')
    im.add_argument('source');im.add_argument('output')
    r=sub.add_parser('run',help='Run the manuscript-based reconstruction, using newly authored prompts')
    r.add_argument('--manifest',required=True);r.add_argument('--config',default=str(ROOT/'config/run.json'))
    r.add_argument('--output',required=True);r.add_argument('--methods',nargs='+',choices=METHODS,default=list(PRIMARY))
    r.add_argument('--mock',action='store_true');r.add_argument('--resume',action='store_true');r.add_argument('--limit',type=int)
    rec=sub.add_parser('recover',help='Export actual prompt messages and observed artifacts from preserved JSONL')
    rec.add_argument('source');rec.add_argument('output')
    a=sub.add_parser('analyze-recorded',help='Recompute primary tests without model inference; needs numpy/scipy')
    a.add_argument('source');a.add_argument('output')
    rep=sub.add_parser('replay',help='Inspect a recorded request; --execute sends it to a local model server')
    rep.add_argument('--example',required=True);rep.add_argument('--base-url',default='http://127.0.0.1:8000/v1')
    rep.add_argument('--output',required=True);rep.add_argument('--execute',action='store_true')
    summary=sub.add_parser('summarize',help='Paired statistical analysis of new runs; never mixed with historical results')
    summary.add_argument('runs',nargs='+');summary.add_argument('--output',required=True)
    summary.add_argument('--bootstrap',type=int,default=10000)
    audit=sub.add_parser('audit-paper',help='Recompute recorded statistics and compare against final ZIP paper table')
    audit.add_argument('--output',required=True)
    doctor=sub.add_parser('doctor',help='Check bundled cohort, configs and optional dependencies')
    args=p.parse_args()
    if args.command=='doctor':
        import importlib.util
        from .core import validate_manifest
        cohort=json.loads((ROOT/'data/recovered/cohort_for_reimplementation.json').read_text())
        rows=validate_manifest(cohort,Schema())
        print(json.dumps({'software':'AdaptivePD','personas':len(rows),'final_paper':(ROOT/'paper/main.tex').is_file(),
          'dependencies':{m:importlib.util.find_spec(m) is not None for m in ('numpy','scipy','vllm','huggingface_hub')},
          'note':'vLLM can be installed in a separate serving environment.'},indent=2))
    elif args.command=='summarize':
        from .reporting import analyze_runs
        result=analyze_runs(args.runs,args.output,args.bootstrap)
        print('Report:',args.output,'kind:',result['artifact_kind'])
    elif args.command=='audit-paper':
        from .paper_audit import audit_paper
        result=audit_paper(args.output)
        print('Final paper match:',result['all_checks_passed'])
        if not result['all_checks_passed']:raise SystemExit(1)
    elif args.command=='manifest':
        exclude=[]
        if args.exclude:exclude=[r['id'] for r in json.loads(Path(args.exclude).read_text())['personas']]
        manifest=make_manifest(Schema(),args.count,args.seed,exclude)
        dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('x') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
        print('Saved NEW cohort:',dest)
    elif args.command=='import-cohort':
        manifest=import_recovered_personas(args.source,Schema())
        with Path(args.output).open('x') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
        print('Imported historical gold values:',len(manifest['personas']))
    elif args.command=='run':
        result=run(json.loads(Path(args.manifest).read_text()),json.loads(Path(args.config).read_text()),
                   args.output,args.methods,args.mock,args.resume,args.limit)
        print('Finished:',result['artifact_kind'])
    elif args.command=='recover':
        from .recover import recover
        result=recover(args.source,args.output);print('Recovered persona identities:',result['historical_personas'])
    elif args.command=='analyze-recorded':
        from .analyze_recovered import analyze
        result=analyze(args.source,args.output);print('Reference match:',result['matches_within_1e_10'])
    else:
        example=json.loads(Path(args.example).read_text());call=example['call']
        request={'model':call['model'],'messages':call['prompt_messages'],'seed':call['seed'],
                 'temperature':call['temperature'],'top_p':call['top_p'],'max_tokens':call['max_new_tokens']}
        result={'kind':'recorded_request_inspection','source':example['source'],'request':request,
            'historical_raw_response':call['raw_response'],'inference_performed':False,
            'limitation':'Checkpoint, tokenizer, chat template and execution runtime must match independently; exact generated response is not guaranteed.'}
        dest=Path(args.output)
        if dest.exists():raise FileExistsError(dest)
        if args.execute:
            headers={'Content-Type':'application/json'}
            if os.getenv('VLLM_API_KEY'):headers['Authorization']='Bearer '+os.environ['VLLM_API_KEY']
            req=urllib.request.Request(args.base_url.rstrip('/')+'/chat/completions',data=json.dumps(request).encode(),headers=headers)
            with urllib.request.urlopen(req,timeout=300) as conn:response=json.load(conn)
            result.update(kind='new_inference_on_recorded_input',inference_performed=True,response=response)
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
        print('Saved:',dest,'inference:',result['inference_performed'])

if __name__=='__main__':main()
