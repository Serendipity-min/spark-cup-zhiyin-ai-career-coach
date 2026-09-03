import yaml, os, json
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 关键：ylm 里有 systemTemplate 字段
# 让我看每个节点的 data 下所有 keys（含嵌套）
for nid_short in ['node-end', 'spark-llm::', 'question-answer::']:
    for n in d['flowData']['nodes']:
        if n['id'].startswith(nid_short):
            alias = n['data']['nodeMeta'].get('aliasName', '?')
            print(f'\n=== {alias} (id={n["id"][:50]}) ===')
            data = n['data']
            # 遍历所有第一层 key
            for k, v in data.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    if isinstance(v, str) and len(v) > 80:
                        print(f'  {k}: ({len(v)} 字符) {v[:50]}...')
                    else:
                        print(f'  {k}: {v}')
                elif isinstance(v, dict):
                    keys = list(v.keys())
                    print(f'  {k}: dict ({len(keys)} keys) - {keys[:8]}')
                elif isinstance(v, list):
                    print(f'  {k}: list ({len(v)} 项)')
            # nodeParam 子节点
            if 'nodeParam' in data:
                np = data['nodeParam']
                print('  --- nodeParam keys ---')
                for k, v in np.items():
                    if isinstance(v, str) and len(v) > 100:
                        print(f'    {k}: ({len(v)} 字符)')
                    elif isinstance(v, dict):
                        print(f'    {k}: dict {list(v.keys())}')
                    elif isinstance(v, list):
                        print(f'    {k}: list ({len(v)})')
                    else:
                        print(f'    {k}: {v}')