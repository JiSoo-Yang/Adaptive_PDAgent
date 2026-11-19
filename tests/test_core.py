import json
import tempfile
import unittest
from pathlib import Path
from pdaccess.core import *
from pdaccess.prompts import clean_choice
from pdaccess.runner import run, METHODS

class Rules(unittest.TestCase):
    def test_grounding_and_merge(self):
        g=Graph()
        update={'nodes':[{'name':'Work','span':'WORK  tasks','dimensions':['social_role']},
                         {'name':'plan','span':'plan daily','dimensions':['social_role']},
                         {'name':'hallucination','span':'not in response','dimensions':[]}],
                'edges':[{'source':'work','target':'plan','relation':'theme','span':'tasks and plan'},
                         {'source':'work','target':'missing','relation':'theme','span':'work'}]}
        g.update(update,'I do Work tasks and plan daily.')
        self.assertEqual(len(g.nodes),2);self.assertEqual(len(g.edges),1)
        self.assertEqual(g.state()['dimensions']['social_role']['status'],'covered')
        self.assertEqual(g.novelties,[1.])
        g.update(update,'I do Work tasks and plan daily.')
        self.assertEqual(g.novelties,[1.,0.]);self.assertEqual(len(g.edges),1)

    def test_json_strings_and_last_object(self):
        self.assertEqual(last_object('text {"a":{"x":"} inside"}} tail {"last":2}'),{'last':2})
        self.assertEqual(last_object('bad {no}'),{})
        self.assertEqual(last_object('```json\n{"ok":1}\n```'),{'ok':1})

    def test_utility_and_stop(self):
        self.assertAlmostEqual(utility({}),-.2)
        self.assertAlmostEqual(utility({'coverage':2,'discrimination':1,'novelty':1,'redundancy':0,'leakage':0}),.8)
        self.assertAlmostEqual(utility({'coverage':float('nan')}),-.2)
        g=Graph();g.update({},'');g.update({},'');state=g.state()
        self.assertTrue(gate(state,2))
        self.assertFalse(selective_stop(state,2,False,'stop',0))
        self.assertTrue(selective_stop(state,3,False,'stop',.24))
        self.assertFalse(selective_stop(state,3,True,'stop',0))
        self.assertFalse(selective_stop(state,3,False,'stop',.25))

    def test_manifest_and_scoring(self):
        schema=Schema();a=make_manifest(schema,304);b=make_manifest(schema,304)
        self.assertEqual(a,b);rows=validate_manifest(a,schema)
        self.assertEqual(len(set(r['id'] for r in rows)),304)
        dev=make_manifest(schema,100,20260801)
        held=make_manifest(schema,304,exclude=[r['id'] for r in dev['personas']])
        self.assertFalse(set(r['id'] for r in dev['personas']) & set(r['id'] for r in held['personas']))
        baselines=majority_baselines(rows)
        row=rows[0];pred={d:v['value'] for d,v in row['persona'].items()}
        self.assertEqual(score_prediction(schema,row['persona'],pred,baselines)['average_gain'],1.)
        self.assertEqual(score_prediction(schema,row['persona'],{},baselines)['correct'],dict.fromkeys(DIMS,0))
        tiny=make_manifest(schema,1)
        self.assertIsNone(score_prediction(schema,tiny['personas'][0]['persona'],pred,majority_baselines(tiny['personas']))['average_gain'])

    def test_parser_no_reranking(self):
        obj={'action':'invalid','target_dimension':'bad','candidates':'bad',
             'selected_question':'What responsibilities occupy most of your day?'}
        c=clean_choice(obj,2,Schema())
        self.assertEqual(c['question'],obj['selected_question']);self.assertFalse(c['fallback'])
        self.assertEqual(c['action'],'explore');self.assertEqual(c['candidates'],[])
        c=clean_choice({'selected_question':'Are you a Doctor?'},2,Schema())
        self.assertTrue(c['fallback'])

    def test_all_methods_mock_and_resume(self):
        schema=Schema();manifest=make_manifest(schema,20)
        config=json.loads((ROOT/'config/run.json').read_text())
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'run'
            summary=run(manifest,config,path,METHODS,mock=True,limit=2)
            rows=[json.loads(l) for l in (path/'results.jsonl').read_text().splitlines()]
            self.assertEqual(len(rows),24)
            for pid in {r['persona_id'] for r in rows}:
                group=[r for r in rows if r['persona_id']==pid]
                self.assertEqual(len({json.dumps(r['history'][0]) for r in group}),1)
                self.assertEqual(len({tuple(r['shared_first_call_ids']) for r in group}),1)
            self.assertTrue(all(not r['tokens_complete'] and r['input_tokens'] is None for r in rows))
            before=(path/'results.jsonl').read_bytes()
            run(manifest,config,path,METHODS,mock=True,resume=True,limit=2)
            self.assertEqual(before,(path/'results.jsonl').read_bytes())
            config['base_seed']+=1
            with self.assertRaises(ValueError):run(manifest,config,path,METHODS,mock=True,resume=True,limit=2)

if __name__=='__main__':unittest.main()

class RecoveredEvidence(unittest.TestCase):
    def test_recorded_initial_and_controller_messages(self):
        from pdaccess import prompts
        self.assertEqual(prompts.messages('initial',{}),prompts.RECORDED['question_generation']['call']['prompt_messages'])
        import re
        for role in ['adaptive','generic','direct','no_coverage','no_redundancy','original','dialogue']:
            example=prompts.RECORDED[prompts.ROLE_MAP[role]]['call']['prompt_messages']
            text=example[-1]['content']
            match=re.search(r'Q1: (.*?)\nA1: (.*?)(?:\n\n)',text,re.S)
            self.assertIsNotNone(match)
            history=[{'question':match.group(1),'answer':match.group(2)}]
            self.assertEqual(prompts.messages(role,{'dialogue':history}),example,role)
        self.assertEqual(sum(map(len,prompts.FALLBACK.values())),15)

    def test_http_transport_request_and_cache(self):
        import threading
        from http.server import BaseHTTPRequestHandler,HTTPServer
        from pdaccess.backend import Backend
        requests=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                data=json.dumps({'choices':[{'message':{'content':'{"ok":true}'}}],
                                 'usage':{'prompt_tokens':12,'completion_tokens':4}}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
            def log_message(self,*args):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            config=json.loads((ROOT/'config/run.json').read_text())
            config['agent']['base_url']=f'http://127.0.0.1:{server.server_port}/v1'
            with tempfile.TemporaryDirectory() as td:
                backend=Backend(config,td)
                messages=[{'role':'user','content':'fixture'}]
                a=backend.complete('adaptive',messages,123)
                b=backend.complete('adaptive',messages,123)
                self.assertEqual(a,b);self.assertEqual(len(requests),1)
                self.assertEqual(requests[0]['max_tokens'],512)
                self.assertEqual(requests[0]['temperature'],.7)
                self.assertEqual(requests[0]['seed'],123)
                self.assertTrue(backend.calls[-1]['cache_reuse'])
        finally:server.shutdown();server.server_close();thread.join()
