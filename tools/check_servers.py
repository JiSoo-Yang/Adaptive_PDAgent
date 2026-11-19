"""Verify served model aliases. HTTP cannot certify loaded checkpoint revision."""
import argparse,json,os,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,default=ROOT/'config/qwen1_7b.json');args=p.parse_args()
    config=json.loads(args.config.read_text())
    for role in ('agent','target'):
        spec=config[role];headers={};token=os.getenv(spec.get('api_key_env','VLLM_API_KEY'))
        if token:headers['Authorization']='Bearer '+token
        request=urllib.request.Request(spec['base_url'].rstrip('/')+'/models',headers=headers)
        with urllib.request.urlopen(request,timeout=15) as r:models=json.load(r)
        ids=[d['id'] for d in models['data']]
        if spec['model'] not in ids:raise ValueError(f'{role}: expected {spec["model"]}, server offers {ids}')
        print(role,'ready:',spec['model'])
    print('Aliases verified; checkpoint revision and runtime must be checked in server launch records.')
if __name__=='__main__':main()
