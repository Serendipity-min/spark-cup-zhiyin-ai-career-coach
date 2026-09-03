import yaml, os, json
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 打印大模型节点完整 JSON 结构
n = next(n for n in d['flowData']['nodes'] if n['id'] == 'spark-llm::b6927f92-d655-4c5d-92ad-deff6af18ba9')
# 完整 dump
print('=== 完整 JSON (前 5000 字符) ===')
s = json.dumps(n, ensure_ascii=False, indent=2)
print(s[:5000])
print('...')
print(f'总长度: {len(s)} 字符')