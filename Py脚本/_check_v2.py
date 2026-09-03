import yaml, os
os.chdir(r'E:\workbuddy_projrct\星火杯')
fn = r'e:\Chrome\职引 · A20260714192539.yml'
d = yaml.safe_load(open(fn, 'r', encoding='utf-8'))
edges = len(d['flowData']['edges'])
nodes = len(d['flowData']['nodes'])
print('=== Newest yml ===')
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
# 重点检查 KB 节点
print()
print('=== KB 节点 ===')
for n in d['flowData']['nodes']:
    if 'knowledge-base' in n['id']:
        alias = n['data']['nodeMeta'].get('aliasName', '?')
        nid = n['id']
        # 输出所有入参连接的目标节点
        in_edges = [e for e in d['flowData']['edges'] if e['target'] == nid]
        out_edges = [e for e in d['flowData']['edges'] if e['source'] == nid]
        print('  KB Node:', alias)
        print('    In edges:', len(in_edges))
        for e in in_edges:
            print('      <-', e['source'][:50])
        print('    Out edges:', len(out_edges))
        for e in out_edges:
            print('      ->', e['target'][:50])