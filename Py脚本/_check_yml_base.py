import yaml, os
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
d = yaml.safe_load(open(fn, 'r', encoding='utf-8'))
print('=== 当前 yml ===')
print('Edges:', len(d['flowData']['edges']))
print('Nodes:', len(d['flowData']['nodes']))
print()
for n in d['flowData']['nodes']:
    print('  ', n['data']['nodeMeta']['nodeType'], '-', n['data']['nodeMeta'].get('aliasName', '?'))