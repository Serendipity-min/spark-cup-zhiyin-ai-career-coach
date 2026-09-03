import yaml, os, json
os.chdir(r'E:\workbuddy_projrct\星火杯')
fn = r'e:\Chrome\职引 · A20260714192539.yml'
d = yaml.safe_load(open(fn, 'r', encoding='utf-8'))

# 输出每个节点的 prompt 内容
for n in d['flowData']['nodes']:
    nid = n['id'][:55]
    typ = n['data']['nodeMeta']['nodeType']
    alias = n['data']['nodeMeta'].get('aliasName', '?')
    print(f'\n{"="*70}')
    print(f'节点类型: {typ}')
    print(f'节点别名: {alias}')
    print(f'节点ID: {nid}')
    print(f'{"="*70}')
    # nodeParams
    params = n['data']['nodeMeta'].get('nodeParams', {})
    # systemPrompt
    sp = params.get('systemPrompt', '')
    if sp:
        print(f'\n【系统提示词】 ({len(sp)} 字符):')
        print('-'*70)
        print(sp[:3000])
    # userPrompt
    up = params.get('userPrompt', '')
    if up:
        print(f'\n【用户提示词】 ({len(up)} 字符):')
        print('-'*70)
        print(up[:3000])
    # inputs
    inputs = params.get('inputs', [])
    if inputs:
        print(f'\n【输入参数】')
        for i, inp in enumerate(inputs, 1):
            val = inp.get('value', {}).get('value', '?') if isinstance(inp.get('value'), dict) else inp.get('value', '?')
            print(f'  {i}. {inp.get("name", "?")} = {val[:200] if isinstance(val, str) else val}')
    # kbConfig
    kb = params.get('kbConfig', [])
    if kb:
        print(f'\n【知识库配置】')
        for i, k in enumerate(kb, 1):
            print(f'  {i}. {k}')
    # outputs
    outputs = params.get('outputs', [])
    if outputs:
        print(f'\n【输出参数】')
        for i, o in enumerate(outputs, 1):
            print(f'  {i}. {o}')