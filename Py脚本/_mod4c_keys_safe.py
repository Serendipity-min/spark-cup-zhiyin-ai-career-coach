# -*- coding: utf-8 -*-
import yaml, os, json, sys
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 强制 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def safe_str(v):
    try:
        return str(v)
    except:
        return repr(v)

for nid_short in ['node-end', 'spark-llm::', 'question-answer::']:
    for n in d['flowData']['nodes']:
        if n['id'].startswith(nid_short):
            alias = n['data']['nodeMeta'].get('aliasName', '?')
            print(f'\n=== {alias} (id={n["id"][:50]}) ===')
            data = n['data']
            for k, v in data.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    if isinstance(v, str) and len(v) > 80:
                        print(f'  {k}: ({len(v)} chars)')
                    else:
                        print(f'  {k}: {v}')
                elif isinstance(v, dict):
                    keys = list(v.keys())
                    print(f'  {k}: dict ({len(keys)} keys) - {keys[:8]}')
                elif isinstance(v, list):
                    print(f'  {k}: list ({len(v)} items)')
            if 'nodeParam' in data:
                np = data['nodeParam']
                print('  --- nodeParam keys ---')
                for k, v in np.items():
                    if isinstance(v, str):
                        if len(v) > 100:
                            print(f'    {k}: ({len(v)} chars)')
                        else:
                            print(f'    {k}: {safe_str(v)}')
                    elif isinstance(v, dict):
                        print(f'    {k}: dict {list(v.keys())}')
                    elif isinstance(v, list):
                        print(f'    {k}: list ({len(v)})')
                    else:
                        print(f'    {k}: {v}')