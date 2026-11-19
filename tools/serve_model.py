"""Start a pinned local checkpoint using vLLM; run in the serving environment."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
ROOT=Path(__file__).resolve().parents[1]

def command(config,role,tensor_parallel=1,max_length=16384):
    from urllib.parse import urlparse
    spec=config[role];url=urlparse(spec['base_url'])
    if url.hostname not in ('localhost','127.0.0.1'):raise ValueError('Local serve helper expects localhost endpoint')
    local=Path(spec.get('local_model_dir','models/'+spec['model'].split('/')[-1]))
    if not local.is_absolute():local=ROOT/local
    return ['vllm','serve',str(local),'--served-model-name',spec['model'],'--host','127.0.0.1','--port',str(url.port or 8000),
            '--dtype','bfloat16','--generation-config','vllm','--tensor-parallel-size',str(tensor_parallel),'--max-model-len',str(max_length)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,default=ROOT/'config/qwen1_7b.json')
    p.add_argument('--role',choices=['agent','target'],required=True);p.add_argument('--tensor-parallel-size',type=int,default=1)
    p.add_argument('--max-model-len',type=int,default=16384);p.add_argument('--dry-run',action='store_true');args=p.parse_args()
    if args.tensor_parallel_size<1 or args.max_model_len<1:raise ValueError('GPU count and context length must be positive')
    config=json.loads(args.config.read_text());cmd=command(config,args.role,args.tensor_parallel_size,args.max_model_len)
    print(shlex.join(cmd),flush=True)
    if args.dry_run:return
    model_dir=Path(cmd[2]);stamp=model_dir/'adaptivepd_download.json'
    if not (model_dir/'config.json').exists():raise FileNotFoundError(f'Download the model first: {model_dir}')
    if stamp.exists() and json.loads(stamp.read_text())['revision']!=config[args.role]['revision']:raise ValueError('Local checkpoint revision differs from config')
    # Resolve vllm beside this Python interpreter, even if the venv was not activated.
    import sys
    executable=Path(sys.executable).parent/'vllm'
    cmd[0]=str(executable) if executable.exists() else shutil.which('vllm') or 'vllm'
    subprocess.run(cmd,check=True)
if __name__=='__main__':main()
