"""Local vLLM-compatible HTTP client, exact call audit, and explicitly synthetic mock."""
import json
import os
import re
import time
import urllib.request
from pathlib import Path
from .core import digest

DECODING={
 'initial':(.7,96), 'original':(.7,96), 'adaptive':(.7,512), 'generic':(.7,512),
 'direct':(.7,512), 'no_coverage':(.7,512), 'no_redundancy':(.7,512),
 'dialogue':(.7,128), 'round_robin':(.7,128), 'online':(.7,640),
 'selective_dialogue':(.7,256), 'selective_graph':(.7,256), 'utility':(0.,256),
 'state':(0.,512), 'extract':(0.,768), 'integrated':(0.,896),
 'target':(.7,256), 'predict':(0.,384), 'uncertainty':(.8,384)}
TEXT_ROLES={'initial','original','dialogue','round_robin','target'}


class Backend:
    def __init__(self, config, directory, mock=False):
        self.config=config
        self.directory=Path(directory)
        self.mock=mock
        self.calls=[]
        self.cache=self.directory/'call_cache'
        self.cache.mkdir(exist_ok=True)

    def complete(self, role, messages, seed, target=False, context=None):
        spec=self.config['target' if target else 'agent']
        temp,limit=DECODING[role]
        request={'model':spec['model'],'messages':messages,'temperature':temp,'top_p':.8,'max_tokens':limit,'seed':seed}
        if role not in TEXT_ROLES:
            request['response_format']={'type':'json_object'}
        if spec.get('chat_template_kwargs'):
            request['chat_template_kwargs']=spec['chat_template_kwargs']
        call_id=digest({'role':role,'request':request,'endpoint':spec['base_url'],'revision':spec['revision'],'mock':self.mock})
        path=self.cache/(call_id+'.json')
        cached=path.exists()
        start=time.monotonic()
        if cached:
            record=json.loads(path.read_text())
        else:
            if self.mock:
                text=self._mock(role,messages)
                response={'choices':[{'message':{'content':text},'finish_reason':'stop'}],
                          'usage':None,'mock':True}
            else:
                headers={'Content-Type':'application/json'}
                token=os.environ.get(spec.get('api_key_env','VLLM_API_KEY'))
                if token:
                    headers['Authorization']='Bearer '+token
                req=urllib.request.Request(spec['base_url'].rstrip('/')+'/chat/completions',
                    data=json.dumps(request).encode(),headers=headers)
                # No silent retries: transport failures stop the run and can be resumed.
                with urllib.request.urlopen(req,timeout=self.config.get('timeout_seconds',300)) as conn:
                    response=json.load(conn)
                text=response['choices'][0]['message'].get('content')
                if not isinstance(text,str):
                    raise ValueError('Backend returned no textual content')
            record={'call_id':call_id,'role':role,'request':request,'response':response,'text':text,
                    'requested_revision':spec['revision'],'revision_verified':False,
                    'backend':'mock_synthetic' if self.mock else 'vllm_compatible_http',
                    'elapsed_seconds':time.monotonic()-start}
            temp_path=path.with_suffix('.tmp')
            temp_path.write_text(json.dumps(record,ensure_ascii=False,indent=2));temp_path.replace(path)
        event={'call_id':call_id,'role':role,'cache_reuse':cached,'context':context or {},
               'usage':record['response'].get('usage')}
        self.calls.append(event)
        with (self.directory/'calls.jsonl').open('a') as f:
            f.write(json.dumps(event,ensure_ascii=False)+'\n')
        return record['text'],call_id

    def _mock(self,role,messages):
        """Synthetic plumbing fixtures. No scientific inference or real token estimates."""
        if role=='target':
            return 'I review tasks and plan with colleagues before starting the day.'
        if role in TEXT_ROLES:
            return 'What responsibilities occupy most of your day?'
        try:
            payload=json.loads(messages[-1]['content'])
        except ValueError:
            payload={'allowed_values':{}}
            for dim,values in re.findall(r'^- (social_role|personality|background|interests)[^:]*: (.*)$',messages[-1]['content'],re.M):
                payload['allowed_values'][dim]=values.split(', ')
        if role in ('extract','integrated'):
            return json.dumps({'nodes':[
                {'name':'tasks','span':'review tasks','dimensions':['social_role']},
                {'name':'colleagues','span':'plan with colleagues','dimensions':['social_role']}],
                'edges':[{'source':'tasks','target':'colleagues','relation':'theme','span':'review tasks and plan with colleagues'}],
                'competitions':[]})
        if role=='state':
            return '{"competitions":[]}'
        if role=='utility':
            return json.dumps({k:{'coverage':.4,'discrimination':.3,'novelty':.3,'redundancy':.2,'leakage':0} for k in ['A','B']})
        if role in ('predict','uncertainty'):
            return json.dumps({k:v[0] for k,v in payload['allowed_values'].items()})
        questions=['What responsibilities occupy most of your day?', 'What experiences have shaped your everyday routine?', 'What do you choose to do when you have time to yourself?']
        return json.dumps({'action':'explore','target_dimension':'background','candidates':[
            {'question':q,'coverage_gain':.5,'redundancy_penalty':.1} for q in questions],
            'selected_question':questions[1],'expected_gain':.4})
