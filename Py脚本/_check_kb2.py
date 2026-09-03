import yaml, json, os
os.chdir(r'E:\workbuddy_projrct\星火杯')
fn = r'e:\Chrome\职引 · A20260714192539 (1).yml'
d = yaml.safe_load(open(fn, 'r', encoding='utf-8'))
for n in d['flowData']['nodes']:
    if 'knowledge-base' in n['id']:
        print('=== KB node full data ===\n')
        # 输出原始 nodeMeta 看看结构
        meta = n['data']['nodeMeta']
        print(json.dumps(meta, ensure_ascii=False, indent=2)[:3000])
        break