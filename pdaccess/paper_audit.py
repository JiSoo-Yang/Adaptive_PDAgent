"""Compare recalculated historical scores with the ACTUAL final paper source."""
import hashlib
import json
import re
from pathlib import Path
from .core import ROOT
from .analyze_recovered import analyze
from .reporting import write_csv


def audit_paper(output):
    dest=Path(output)
    if dest.exists():raise FileExistsError(dest)
    dest.mkdir(parents=True)
    report=analyze(ROOT/'data/recorded',dest/'recalculated')
    source=(ROOT/'paper/main.tex').read_text()
    primary_table=source.split('\\label{tab:primary',1)
    # Match only the four numeric primary rows, not descriptions or other tables.
    table_rows=[]
    for line in source.splitlines():
        if re.match(r'^(Qwen3-1\.7B|Qwen3-4B|Llama-3\.2-3B-Instruct|Gemma-3-4B-IT) & 304 & ',line):
            table_rows.append(line)
    if len(table_rows)!=4:raise ValueError('Could not locate four primary rows in final main.tex')
    def canonical(name):return name.lower().replace('-instruct','').replace('-it','').split('/')[-1]
    checks=[]
    for line in table_rows:
        fields=[s.strip().strip('$') for s in line.split('&')]
        name=canonical(fields[0]);rows=[r for r in report['primary'] if canonical(r['target'])==name]
        if len(rows)!=1:raise ValueError('Unmatched target '+fields[0])
        row=rows[0];ci=re.findall(r'[+-]?\d+\.\d+',fields[6])
        mapping={'n':fields[1],'original':fields[3],'adaptive':fields[4],'delta':fields[5],
                 'ci_low':ci[0],'ci_high':ci[1],'W':fields[7],'p':fields[8],'p_bh':fields[9]}
        for key,text in mapping.items():
            expected=float(text);places=len(text.split('.')[1]) if '.' in text else 0
            tolerance=.5*10**(-places)+1e-12
            error=abs(row[key]-expected)
            checks.append({'target':fields[0],'metric':key,'final_paper':expected,'recalculated':row[key],'tolerance':tolerance,'absolute_error':error,'passed':error<=tolerance})
        n_eff=int(fields[2]);checks.append({'target':fields[0],'metric':'n_nonzero','final_paper':n_eff,'recalculated':row['n']-row['ties'],'passed':row['n']-row['ties']==n_eff})
    final={'kind':'historical_score_reanalysis_against_final_paper','inference_performed':False,
           'paper_sha256':hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest(),
           'all_checks_passed':all(c['passed'] for c in checks) and report['matches_within_1e_10'],
           'reference_inputs_match':report['matches_within_1e_10'],'checks':checks,
           'limitation':'Recomputes retained binary scores and paired statistics; does not rerun models or recover the historical label scorer.'}
    (dest/'final_paper_audit.json').write_text(json.dumps(final,indent=2)+'\n')
    write_csv(dest/'final_paper_comparison.csv',checks)
    return final
