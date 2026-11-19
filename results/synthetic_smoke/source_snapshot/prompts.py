"""Draft reconstruction prompts plus recovery-aware adapters. See RECORDED and ROLE_MAP below."""
import json
import re
from pathlib import Path
from .core import ROOT
from .core import DIMS, RELATIONS, norm

FALLBACK = {
 'social_role': ['What responsibilities occupy most of your day?', 'What decisions do others usually rely on you to make?', 'Describe a recent challenge and your part in resolving it.'],
 'personality': ['How do you react when a familiar plan changes unexpectedly?', 'How do you approach a task that has no clear instructions?', 'What do you do when people disagree about how to proceed?'],
 'background': ['What experiences have shaped your everyday routine?', 'How has your daily routine changed over the years?', 'Describe the surroundings in which you spend most of your time.'],
 'interests': ['What do you choose to do when you have time to yourself?', 'What makes an activity worth returning to for you?', 'What do you enjoy finding out more about, and why?'],
 'generic': ['Describe something that mattered to you recently.', 'What guides the choices you make in an ordinary day?', 'What part of your routine would you most like to change?']}
FORBIDDEN = ('system prompt','persona label','ground truth','hidden persona','candidate label')

SYSTEM = {
 'initial': 'Ask one natural, open-ended introductory question to learn about an unfamiliar person. Do not name persona labels or ask them to identify a category. Return only the question.',
 'original': 'Ask one natural, general open-ended follow-up based on the dialogue. Do not name persona labels or ask them to identify a category. Return only the question.',
 'target': 'Respond naturally as the person described by the private persona. Express the characteristics through behavior, responsibilities and preferences. Do not list the supplied labels, disclose the persona instruction, or announce your assigned role. Answer the interviewer in English.',
 'adaptive': '''You select the next indirect interview question using dialogue history only. Review evidence for social_role, personality, background and interests. Focus on an unresolved or ambiguous dimension. Generate exactly three coherent candidate questions seeking new evidence and avoiding repetition. Judge each candidate's coverage_gain and redundancy_penalty, then select a question yourself. Do not reveal schema labels in the question. If sufficient evidence has been obtained, you may return action stop. Return JSON: {"action":"explore or stop","target_dimension":"dimension or null","candidates":[{"question":"text","coverage_gain":0,"redundancy_penalty":0}],"selected_question":"text"}. The zeros show numeric field types, not an anchored scale or scoring rubric. Do not use a fixed weighted formula.''',
 'generic': '''Generate exactly three conversationally specific follow-up candidates from the dialogue. Assess only conversational specificity and repetition; do not assess persona coverage or select a persona dimension. Select a question yourself. Return JSON with action explore, target_dimension null, candidates (question, specificity, repetition), and selected_question. Do not ask for or name persona labels.''',
 'direct': 'Select an unresolved persona dimension from the dialogue and generate one coherent indirect question seeking new evidence without repetition. Return JSON with action (explore or stop), target_dimension and selected_question. Do not generate a candidate list. Do not expose schema labels.',
 'dialogue': 'Generate one specific natural follow-up from the recent dialogue. Return only the question. Do not mention persona labels or use explicit ranking, coverage, redundancy or target-dimension fields.',
 'round_robin': 'Ask one indirect behavioral follow-up about the supplied focus dimension, coherently connected to the dialogue. Return only the question, without naming persona labels.',
 'extract': '''Extract grounded concepts and implicit bridging relations from CURRENT_RESPONSE, using earlier dialogue/graph only as context. Return JSON {"nodes":[{"name":"short concept","span":"exact substring of current response","dimensions":["social_role"]}],"edges":[{"source":"concept name","target":"concept name","relation":"part-of","span":"exact substring of current response"}],"competitions":[]}. Dimensions may be social_role, personality, background, interests. Relations may be part-of, member-of, instrument, theme, cause-of, in, temporal. Include only concepts and edges supported by current-response spans. Reuse canonical names; do not substitute synonyms merely because they seem related. A competition, if retained, has alternatives (at least two distinct readings), spans (at least two distinct retained node-support spans), and discriminator (a concrete unanswered question distinguishing them). Omit unsupported competition. Return only JSON.''',
 'state': 'Analyze the supplied grounded graph and dialogue for distinct competing persona interpretations. Return JSON {"competitions":[{"alternatives":["reading 1","reading 2"],"spans":["retained support 1","retained support 2"],"discriminator":"unanswered distinguishing evidence"}]}. Include only grounded alternatives and use exact retained node-support spans. No hidden gold persona is available.',
 'online': 'Use the supplied dialogue, incremental graph and evidence state to select an indirect follow-up that resolves missing evidence or grounded ambiguity. You may stop when enough evidence is present. Return JSON with action (explore or stop), target_dimension and selected_question. Do not reveal persona labels.',
 'selective_dialogue': 'Use only the dialogue to propose one coherent indirect question seeking unresolved persona evidence. Return JSON with action (explore or stop), target_dimension, selected_question, expected_gain (a judgment between 0 and 1). Do not name persona labels.',
 'selective_graph': 'Use the supplied grounded state, graph and dialogue to propose one indirect question resolving competing interpretations or a partially supported dimension. Return JSON with target_dimension and selected_question. Do not name the candidate persona labels.',
 'utility': 'Assess questions A and B without assuming their source. Return JSON with keys A and B, each containing coverage, discrimination, novelty, redundancy, leakage. Each component is between 0 and 1. Leakage penalizes leading wording or revealing candidate persona labels. Return only JSON.',
 'predict': 'Infer the persona values from the dialogue and accumulated bridging graph. Use only the supplied finite candidate-value sets; do not invent labels. Return JSON with social_role, personality, background, interests, each a single value string. Trait/category identities are supplied, but their hidden values are not. Return only JSON.',
 'uncertainty': 'Infer the four persona values from the dialogue. Use the supplied finite candidate sets and return one sampled JSON prediction with social_role, personality, background, interests as single value strings. No hidden gold values are provided.'}
# Component ablations remove the corresponding instruction and field (new wording).
SYSTEM['no_coverage'] = SYSTEM['adaptive'].replace('Review evidence for social_role, personality, background and interests. Focus on an unresolved or ambiguous dimension. ', '').replace('seeking new evidence and avoiding repetition','avoiding repetition').replace("coverage_gain and redundancy_penalty",'redundancy_penalty').replace('"coverage_gain":0,','')
SYSTEM['no_redundancy'] = SYSTEM['adaptive'].replace(' and avoiding repetition','').replace('coverage_gain and redundancy_penalty','coverage_gain').replace(',"redundancy_penalty":0','')


def messages(role, payload):
    return [{'role':'system','content':SYSTEM[role]}, {'role':'user','content':json.dumps(payload,ensure_ascii=False)}]


def target_messages(persona, history, question):
    result=[{'role':'system','content':SYSTEM['target']+'\nPRIVATE_PERSONA: '+json.dumps(persona,ensure_ascii=False)}]
    for row in history:
        result += [{'role':'user','content':row['question']},{'role':'assistant','content':row['answer']}]
    return result+[{'role':'user','content':question}]


def valid_question(question, schema):
    if not isinstance(question,str) or not question.strip():
        return False
    q=norm(question)
    if any(t in q for t in FORBIDDEN):
        return False
    # NEW leakage detector: all schema values >=4 characters, whole-phrase matching.
    # yes/no excluded. This is deliberately recorded as a reconstruction choice.
    labels=[v for d in ('social_role','background','interests') for values in schema.categories(d).values() for v in values]
    return not any(len(norm(v))>=4 and re.search(r'(?<!\w)'+re.escape(norm(v))+r'(?!\w)',q) for v in labels)


def parse_action(obj):
    action=norm(obj.get('action',''))
    return action if action in ('explore','stop') else 'explore'


def clean_choice(obj, next_turn, schema):
    dimension=obj.get('target_dimension')
    dimension=dimension if dimension in DIMS else None
    question=obj.get('selected_question','')
    question=question.strip().strip('"') if isinstance(question,str) else ''
    fallback=not valid_question(question,schema)
    if fallback:
        question=FALLBACK[dimension or 'generic'][(next_turn-1)%3]
    return {'action':parse_action(obj),'target_dimension':dimension,'question':question,
            'fallback':fallback,'candidates':obj.get('candidates') if isinstance(obj.get('candidates'),list) else []}


# Recovery-aware adapter. Original call examples are stored verbatim with source references.
# Runtime serialization and unobserved Online/Selective prompts remain reconstruction choices.
RECORDED = json.loads((ROOT/'config/recorded_prompt_examples.json').read_text())
FALLBACK = json.loads((ROOT/'config/observed_fallback_bank.json').read_text())['questions']
ROLE_MAP = {
 'initial':'question_generation','original':'original_question_generation',
 'adaptive':'dialogue_action_question_selection','generic':'controller_matched_generic_selection',
 'direct':'adaptive_direct_question_selection','no_coverage':'adaptive_no_coverage_question_selection',
 'no_redundancy':'adaptive_no_redundancy_question_selection',
 'dialogue':'dialogue_followup_question_generation','round_robin':'round_robin_question_generation',
 'extract':'graph_extraction','predict':'final_persona_prediction','uncertainty':'uncertainty_prediction'}
_DRAFT_MESSAGES = messages

def _dialogue(history):
    return '\n'.join(f"Q{i}: {r['question']}\nA{i}: {r['answer']}" for i,r in enumerate(history,1))

def _allowed(payload):
    cats=payload['categories'];values=payload['allowed_values']
    return ('- social_role: '+', '.join(values['social_role'])+'\n'
       +'- personality trait "'+cats['personality']+'": '+', '.join(values['personality'])+'\n'
       +'- background category "'+cats['background']+'": '+', '.join(values['background'])+'\n'
       +'- interests category "'+cats['interests']+'": '+', '.join(values['interests']))

def _prediction_schema(cats):
    return ('{\n  "social_role": "...",\n'
      +'  "personality": {"trait": "'+cats['personality']+'", "value": "yes or no"},\n'
      +'  "background": {"category": "'+cats['background']+'", "value": "..."},\n'
      +'  "interests": {"category": "'+cats['interests']+'", "value": "..."}\n}')

def messages(role,payload):
    if role not in ROLE_MAP:
        return _DRAFT_MESSAGES(role,payload)
    example=RECORDED[ROLE_MAP[role]]['call']['prompt_messages']
    system=example[0]['content'];user=example[-1]['content']
    history=payload.get('dialogue',[])
    if role in ('original','dialogue','round_robin'):
        if role=='round_robin':system=system.replace('social_role evidence',payload['focus_dimension']+' evidence')
        user='Conversation so far:\n'+_dialogue(history)+f"\n\nAsk question {len(history)+1} of 5."
    elif role in ('adaptive','generic','direct','no_coverage','no_redundancy'):
        tail=user.split('\n\n',1)[1]
        user=f"Completed turns: {len(history)}/5\nDialogue:\n"+_dialogue(history)+'\n\n'+tail
    elif role=='extract':
        tail=user.split('\n\nReturn:',1)[1]
        names=[n['name'] for n in payload['previous_graph']['nodes']]
        user=('Latest question: '+payload['question']+'\nLatest Target response: '+payload['CURRENT_RESPONSE']
              +'\nPreviously known concepts: '+json.dumps(names,ensure_ascii=False)+'\n\nReturn:'+tail)
    elif role in ('predict','uncertainty'):
        user='Interview:\n'+json.dumps(history,ensure_ascii=False)
        if role=='predict':
            g=payload['graph']
            graph={'concepts':{n['name']:{'dimensions':n['dimensions'],'evidence':[{'supporting_span':s} for s in n['spans']]} for n in g['nodes']},
                   'edges':[{'source':e['source'],'target':e['target'],'relation_type':e['relation'],'supporting_span':s} for e in g['edges'] for s in e['spans']]}
            user+='\n\nGrounded bridging graph:\n'+json.dumps(graph,ensure_ascii=False)
        user+='\n\nAllowed values:\n'+_allowed(payload)+'\n\nReturn exactly:\n'+_prediction_schema(payload['categories'])
    return [{'role':'system','content':system},{'role':'user','content':user}]

def target_messages(persona,history,question):
    system=('Privately role-play a person with these characteristics:\n'
        +'Social role: '+persona['social_role']['value']+'\n'
        +'Personality: '+json.dumps({persona['personality']['category']:persona['personality']['value']})+'\n'
        +'Background: '+json.dumps({persona['background']['category']:persona['background']['value']})+'\n'
        +'Interests: '+json.dumps({persona['interests']['category']:persona['interests']['value']})+'\n\n'
        +RECORDED['target_response']['call']['prompt_messages'][0]['content'].split('\n\n',1)[1])
    result=[{'role':'system','content':system}]
    for r in history:result += [{'role':'user','content':r['question']},{'role':'assistant','content':r['answer']}]
    return result+[{'role':'user','content':question}]


# New reconstruction of the manuscript's integrated extraction/state role.
# The historical Selective prompt was not recovered; keep this explicit.
SYSTEM['integrated'] = SYSTEM['extract'] + " Also inspect previous_graph and earlier_dialogue for competing interpretations. Return competitions only when two distinct retained support spans ground two different readings and provide a concrete unanswered discriminator. Newly extracted nodes/edges must still cite the current response; deterministic host code computes coverage and novelty."
