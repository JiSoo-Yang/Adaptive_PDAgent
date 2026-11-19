"""Deterministic manuscript rules and explicitly reconstructed sampling/matching."""
import hashlib
import json
import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMS = ('social_role', 'personality', 'background', 'interests')
RELATIONS = ('part-of', 'member-of', 'instrument', 'theme', 'cause-of', 'in', 'temporal')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def seed_for(*parts):
    """NEW derivation, not the unavailable historical generation/sampling seed derivation."""
    return int(digest(parts)[:8], 16) & 0x7fffffff


def norm(text):
    return ' '.join(str(text).casefold().split())


def label_norm(text):
    text = unicodedata.normalize('NFKC', str(text)).casefold()
    text = text.replace('’', "'").replace('–', '-').replace('—', '-')
    return ' '.join(re.sub(r'[^\w\s]', ' ', text).split())


def last_object(text):
    """Last balanced top-level JSON object; braces inside strings are ignored."""
    depth = 0
    start = None
    quoted = escaped = False
    found = None
    for i, c in enumerate(str(text)):
        if depth and quoted:
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
            continue
        if depth and c == '"':
            quoted = True
        elif c == '{':
            if depth == 0:
                start = i
            depth += 1
        elif c == '}' and depth:
            depth -= 1
            if depth == 0:
                found = str(text)[start:i+1]
    try:
        result = json.loads(found or '{}')
        return result if isinstance(result, dict) else {}
    except (ValueError, TypeError):
        return {}


def clamp(value, default=0.0):
    try:
        x = float(value)
        return min(1., max(0., x)) if math.isfinite(x) else default
    except (ValueError, TypeError):
        return default


def utility(obj):
    obj = obj if isinstance(obj, dict) else {}
    return round(.30*clamp(obj.get('coverage')) + .25*clamp(obj.get('discrimination'))
                 + .25*clamp(obj.get('novelty')) - .15*clamp(obj.get('redundancy'), 1.)
                 - .05*clamp(obj.get('leakage'), 1.), 6)


class Schema:
    def __init__(self, path=None):
        self.data = json.loads(Path(path or ROOT/'config/persona_schema.json').read_text())
        self.structure = self.data['structure']
        self.roles = self.categories('social_role')
        self.role_category = {norm(v): k for k, vs in self.roles.items() for v in vs}
        self.traits = [next(iter(t)) for t in self.structure['personality']['categories']]

    def categories(self, dim):
        return {k: v['examples'] for k, v in self.structure[dim]['categories'].items()}

    def labels(self, dim, category=None):
        if dim == 'social_role':
            return [v for vs in self.roles.values() for v in vs]
        if dim == 'personality':
            return ['yes', 'no']
        return self.categories(dim)[category]

    def inventory(self, persona):
        return {d: self.labels(d, persona[d]['category']) if d != 'social_role'
                else self.labels(d) for d in DIMS}

    def sample(self, seed, index, nonce):
        rng = random.Random(seed_for('sampler-v1', seed, index, nonce))
        row = {}
        for d in DIMS:
            if d == 'personality':
                category = rng.choice(self.traits)
                value = rng.choice(['yes', 'no'])
            else:
                categories = self.categories(d)
                category = rng.choice(sorted(categories))
                value = rng.choice(categories[category])
            row[d] = {'category': category, 'value': value}
        return row

    def match(self, prediction, labels):
        """NEW normalized nearest-label mapping. Empty output remains invalid."""
        if not isinstance(prediction, str) or not prediction.strip():
            return None
        exact = {label_norm(x): x for x in labels}
        key = label_norm(prediction)
        if key in exact:
            return exact[key]
        # A deterministic similarity fallback, not claimed as the historical implementation.
        return max(labels, key=lambda x: (SequenceMatcher(None, key, label_norm(x)).ratio(), -labels.index(x)))


def make_manifest(schema, count=304, seed=20260802, exclude=()):
    if count < 1:
        raise ValueError('count must be positive')
    occupied = set(exclude)
    rows = []
    for index in range(count):
        for nonce in range(100000):
            persona = schema.sample(seed, index, nonce)
            ident = digest(persona)
            if ident not in occupied:
                occupied.add(ident)
                rows.append({'id': ident, 'index': index, 'nonce': nonce, 'persona': persona})
                break
        else:
            raise RuntimeError('Unable to sample a unique persona')
    return {'kind': 'new_reconstruction_cohort', 'sampler': 'sha256-python-random-v1',
            'seed': seed, 'schema_sha256': digest(schema.data), 'excluded_ids': sorted(exclude),
            'personas': rows, 'historical_manifest': False}


def validate_manifest(manifest, schema):
    rows = manifest['personas']
    if not rows or manifest.get('schema_sha256') != digest(schema.data):
        raise ValueError('Empty cohort or different schema')
    ids = set()
    for row in rows:
        persona = row['persona']
        if row['id'] != digest(persona) or row['id'] in ids:
            raise ValueError('Persona identity mismatch or duplicate')
        ids.add(row['id'])
        for d in DIMS:
            category, value = persona[d]['category'], persona[d]['value']
            if d == 'personality':
                assert category in schema.traits and value in ['yes','no']
            else:
                assert value in schema.categories(d)[category]
    return rows


def majority_baselines(rows):
    counts = {d: defaultdict(Counter) for d in DIMS}
    for row in rows:
        for d, x in row['persona'].items():
            group = 'all' if d == 'social_role' else x['category']
            value = x['category'] if d == 'social_role' else x['value']
            counts[d][group][value] += 1
    return {d: sum(max(c.values()) for c in groups.values())/len(rows) for d, groups in counts.items()}


def score_prediction(schema, persona, prediction, baselines):
    scores, mapped = {}, {}
    for d in DIMS:
        raw = prediction.get(d) if isinstance(prediction, dict) else None
        if isinstance(raw, dict):
            raw = raw.get('value')
        value = schema.match(raw, schema.labels(d, persona[d]['category']))
        mapped[d] = value
        if d == 'social_role':
            scores[d] = int(schema.role_category.get(norm(value)) == persona[d]['category'])
        else:
            scores[d] = int(value is not None and label_norm(value) == label_norm(persona[d]['value']))
    # Tiny smoke cohorts can have a majority baseline of one. Do not fabricate AG then.
    gains = {d: (scores[d]-baselines[d])/(1-baselines[d]) if baselines[d]<1 else None for d in DIMS}
    ag = sum(gains.values())/4 if all(v is not None for v in gains.values()) else None
    return {'correct': scores, 'mapped': mapped, 'gain': gains, 'average_gain': ag}


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.novelties = []
        self.competitions = []
        self.rejected = []

    def update(self, obj, response):
        """NEW JSON schema, with manuscript normalized-span and merge rules."""
        if 'concepts' in obj and isinstance(obj['concepts'],list):
            obj = dict(obj)
            obj['nodes'] = [dict(n,span=n.get('supporting_span')) for n in obj['concepts'] if isinstance(n,dict)]
            obj['edges'] = [dict(e,span=e.get('supporting_span'),relation=e.get('relation_type')) for e in obj.get('edges',[]) if isinstance(e,dict)]
        before = len(self.nodes)+len(self.edges)
        text = norm(response)
        def grounded(span):
            return isinstance(span,str) and bool(norm(span)) and norm(span) in text
        for node in obj.get('nodes', []) if isinstance(obj.get('nodes'),list) else []:
            if not isinstance(node,dict) or not isinstance(node.get('name'),str) or not norm(node['name']) or not grounded(node.get('span')):
                self.rejected.append({'kind':'node','reason':'missing name or ungrounded span'})
                continue
            key = norm(node['name'])
            current = self.nodes.setdefault(key, {'name':key,'spans':[], 'dimensions':[]})
            span = norm(node['span'])
            if span not in current['spans']:
                current['spans'].append(span)
            for d in node.get('dimensions',[]) if isinstance(node.get('dimensions'),list) else []:
                if d in DIMS and d not in current['dimensions']:
                    current['dimensions'].append(d)
        for edge in obj.get('edges', []) if isinstance(obj.get('edges'),list) else []:
            if not isinstance(edge,dict):
                continue
            src, dst, rel = norm(edge.get('source','')), norm(edge.get('target','')), edge.get('relation')
            if src not in self.nodes or dst not in self.nodes or rel not in RELATIONS or not grounded(edge.get('span')):
                self.rejected.append({'kind':'edge','reason':'missing endpoint, invalid relation or ungrounded span'})
                continue
            key = (src,rel,dst)
            current = self.edges.setdefault(key, {'source':src,'relation':rel,'target':dst,'spans':[]})
            span=norm(edge['span'])
            if span not in current['spans']:
                current['spans'].append(span)
        after = len(self.nodes)+len(self.edges)
        self.novelties.append((after-before)/max(1,after))
        # Reconstructed competition schema: two distinct readings, two observed spans, discriminator.
        self.competitions = []
        retained = {s for n in self.nodes.values() for s in n['spans']}
        for item in obj.get('competitions',[]) if isinstance(obj.get('competitions'),list) else []:
            if not isinstance(item,dict):
                continue
            alts=item.get('alternatives',[]); spans=item.get('spans',[])
            if (isinstance(alts,list) and len({norm(x) for x in alts if isinstance(x,str)})>=2
                and isinstance(spans,list) and len({norm(s) for s in spans if isinstance(s,str) and norm(s) in retained})>=2
                and isinstance(item.get('discriminator'),str) and item['discriminator'].strip()):
                self.competitions.append(item)

    def payload(self):
        return {'nodes':list(self.nodes.values()),'edges':list(self.edges.values())}

    def state(self):
        dimensions={}
        for d in DIMS:
            names={k for k,n in self.nodes.items() if d in n['dimensions']}
            spans=sorted({s for k in names for s in self.nodes[k]['spans']})[:12]
            n=len(names); e=sum(x['source'] in names or x['target'] in names for x in self.edges.values()); s=len(spans)
            status='missing' if n==0 else 'covered' if n>=2 and (e>=1 or s>=2) else 'partial'
            dimensions[d]={'status':status,'confidence':min(1,.25*n+.15*e+.10*min(s,2)),
                           'concepts':n,'edges':e,'spans':spans}
        return {'dimensions':dimensions, 'novelty':self.novelties[-1] if self.novelties else 0,
                'previous_novelty':self.novelties[-2] if len(self.novelties)>1 else None,
                'competitions':self.competitions}


def gate(state, turn):
    ds=state['dimensions'].values()
    partial=any(d['status']=='partial' and d['spans'] and d['confidence']>=.35 for d in ds)
    stagnant=(turn>=2 and state['previous_novelty'] is not None and state['previous_novelty']<=.10
              and state['novelty']<=.10 and any(d['status']!='covered' for d in ds))
    return bool(state['competitions'] or partial or stagnant)


def selective_stop(state, turn, selected_graph, dialogue_action, gain):
    if turn<3 or selected_graph or state['competitions']:
        return False
    if all(d['status']=='covered' for d in state['dimensions'].values()):
        return True
    return (dialogue_action=='stop' and state['previous_novelty'] is not None
            and state['previous_novelty']<=.10 and state['novelty']<=.10
            and not any(d['status']=='partial' and d['spans'] for d in state['dimensions'].values())
            and gain<.25)


def import_recovered_personas(path, schema):
    """Keep historical gold values, with a new internal ID and preserved historical source ID."""
    rows=[]
    for line in Path(path).read_text().splitlines():
        recorded=json.loads(line);gold=recorded['ground_truth'];persona={}
        role=gold['social_role'];persona['social_role']={'category':schema.role_category[norm(role)],'value':role}
        for d in ('personality','background','interests'):
            x=gold[d];category=x.get('trait') if d=='personality' else x['category']
            # Only punctuation/case-normalized equivalence is allowed for imported gold.
            allowed=schema.labels(d,category)
            matches=[v for v in allowed if label_norm(v)==label_norm(x['value'])]
            if len(matches)!=1:raise ValueError(('Unrecognized recorded gold label',d,x))
            persona[d]={'category':category,'value':matches[0]}
        rows.append({'id':digest(persona),'source_id':recorded['persona_id'],
                     'index':recorded['persona_index'],'persona':persona,'source':recorded['source']})
    result={'kind':'cohort_recovered_from_recorded_gold','sampler':None,'historical_manifest':False,
            'historical_persona_values':True,'seed':20260802,'schema_sha256':digest(schema.data),
            'source_file_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'note':'Reconstructed serialization, not the original heldout_personas.jsonl byte stream. Initial responses are generated anew by run; recorded initial calls can be inspected with replay.',
            'personas':rows}
    validate_manifest(result,schema)
    return result
