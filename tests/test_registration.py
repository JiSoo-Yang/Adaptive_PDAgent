import json
from pathlib import Path
import tempfile
import unittest
from pdaccess.core import ROOT, Graph
from pdaccess.runner import run
from pdaccess.reporting import load_runs, paired_effect, analyze_runs
from pdaccess import prompts

class RegistrationTests(unittest.TestCase):
    def test_integrated_prompt_requests_grounded_competition(self):
        messages=prompts.messages('integrated',{'CURRENT_RESPONSE':'I plan with colleagues.','earlier_dialogue':[],'previous_graph':{'nodes':[],'edges':[]}})
        self.assertIn('competitions',messages[0]['content'])
        self.assertIn('discriminator',messages[0]['content'])
        self.assertIn('current response',messages[0]['content'])

    def test_adaptive_prompt_excludes_graph(self):
        messages=prompts.messages('adaptive',{'dialogue':[{'question':'Routine?','answer':'I plan daily.'}],'graph':{'secret_marker':42}})
        self.assertNotIn('secret_marker',json.dumps(messages))

    def test_grounded_competition_activates_gate(self):
        from pdaccess.core import gate
        graph=Graph();graph.update({'nodes':[{'name':'patient','span':'patient','dimensions':['social_role']},{'name':'results','span':'results','dimensions':['social_role']}],
          'edges':[],'competitions':[{'alternatives':['clinical work','research work'],'spans':['patient','results'],'discriminator':'Do you make treatment decisions?'}]},'I review patient results.')
        self.assertTrue(gate(graph.state(),1));self.assertEqual(len(graph.competitions),1)

    def test_pair_statistics_ties_and_direction(self):
        try:import scipy
        except ImportError:self.skipTest('Install requirements-analysis.txt')
        ties=paired_effect([0,1],[0,1],42,100)
        self.assertEqual(ties['p_raw'],1);self.assertEqual(ties['difference'],0)
        positive=paired_effect([0]*10,[1]*10,42,100)
        self.assertEqual(positive['difference'],1);self.assertEqual(positive['ci_low'],1)
        self.assertEqual(positive['positive'],10)

    def test_mock_report_and_pairing_rejection(self):
        try:import scipy
        except ImportError:self.skipTest('Install requirements-analysis.txt')
        manifest=json.loads((ROOT/'data/recovered/cohort_for_reimplementation.json').read_text())
        config=json.loads((ROOT/'config/qwen1_7b.json').read_text())
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'run';run(manifest,config,output,mock=True,limit=2)
            report=analyze_runs([output],Path(td)/'report',100)
            self.assertEqual(report['artifact_kind'],'synthetic_smoke_only')
            self.assertEqual(len(report['metrics']),4)
            self.assertTrue(all(m['mean_input_tokens'] is None for m in report['metrics']))
            records=[json.loads(l) for l in (output/'results.jsonl').read_text().splitlines()]
            records[1]['history'][0]['answer']='Mismatched first response'
            (output/'results.jsonl').write_text('\n'.join(json.dumps(r) for r in records)+'\n')
            with self.assertRaises(ValueError):load_runs([output])

    def test_model_configs_match_paper_revisions(self):
        text=(ROOT/'paper/main.tex').read_text().replace('\\allowbreak{}','')
        catalog=json.loads((ROOT/'config/models.json').read_text())
        for item in catalog.values():self.assertIn(item['revision'],text)
        for alias in ('qwen1_7b','qwen4b','llama3b','gemma4b'):
            config=json.loads((ROOT/'config'/f'{alias}.json').read_text())
            self.assertEqual(config['target']['model'],catalog[alias]['repository'])
            self.assertEqual(config['budget'],5)
