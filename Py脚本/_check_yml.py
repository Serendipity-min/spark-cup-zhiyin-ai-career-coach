import yaml, os
os.chdir(r'E:\workbuddy_projrct\星火杯')
fn = r'e:\Chrome\职引 · A20260714192539 (1).yml'
d = yaml.safe_load(open(fn, 'r', encoding='utf-8'))
edges = len(d['flowData']['edges'])
nodes = len(d['flowData']['nodes'])
print('=== Latest yml ===')
print('Edges:', edges, 'Nodes:', nodes)
print()
print('=== Nodes ===')
for n in d['flowData']['nodes']:
    typ = n['data']['nodeMeta']['nodeType']
    nid = n['id'][:55]
    print('  ', typ, nid)
print()
print('=== Edges ===')
for i, e in enumerate(d['flowData']['edges'], 1):
    src = e['source'][:45]
    tgt = e['target'][:45]
    print('  ', i, '.', src, '->', tgt)