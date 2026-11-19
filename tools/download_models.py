"""Download paper-pinned checkpoints. No inference and no embedded credentials."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    catalog=json.loads((ROOT/'config/models.json').read_text())
    p=argparse.ArgumentParser();p.add_argument('models',nargs='+',choices=list(catalog));p.add_argument('--dry-run',action='store_true');args=p.parse_args()
    for name in args.models:
        spec=catalog[name];dest=ROOT/spec['directory']
        print(spec['repository'],spec['revision'],'->',dest,flush=True)
        if args.dry_run:continue
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id=spec['repository'],revision=spec['revision'],local_dir=str(dest))
        (dest/'adaptivepd_download.json').write_text(json.dumps(spec,indent=2)+'\n')
if __name__=='__main__':main()
