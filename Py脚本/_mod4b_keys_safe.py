import yaml, os, json
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

for nid_short in ['node-end', 'spark-llm::', 'question-answer::']:
    for n in d['flowData']['nodes']:
        if n['id'].startswith(nid_short):
            alias = n['data']['nodeMeta'].get('aliasName', '?')
            print(f'\n=== {alias} (id={n["id"][:50]}) ===', flush=True)
            data = n['data']
            for k, v in data.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    if isinstance(v, str) and len(v) > 80:
                        print(f'  {k}: ({len(v)} chars)', flush=True)
                    else:
                        print(f'  {k}: {v}', flush=True)
                elif isinstance(v, dict):
                    keys = list(v.keys())
                    print(f'  {k}: dict ({len(keys)} keys) - {keys[:8]}', flush=True)
                elif isinstance(v, list):
                    print(f'  {k}: list ({len(v)} items)', flush=True)
            if 'nodeParam' in data:
                np = data['nodeParam']
                print('  --- nodeParam keys ---', flush=True)
                for k, v in np.items():
                    if isinstance(v, str):
                        if len(v) > 100:
                            print(f'    {k}: ({len(v)} chars)', flush=True)
                        else:
                            print(f'    {k}: {repr(v)}', flush=True)
                    elif isinstance(v, dict):
                        print(f'    {k}: dict {list(v.keys())}', flush=True)
                    elif isinstance(v, list):
                        print(f'    {k}: list ({len(v)})', flush=True)
                    else:
                        print(f'    {k}: {v}', flush=True)