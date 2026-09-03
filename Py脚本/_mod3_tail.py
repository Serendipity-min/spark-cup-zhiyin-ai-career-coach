import yaml, os, json
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

n = next(n for n in d['flowData']['nodes'] if n['id'] == 'spark-llm::b6927f92-d655-4c5d-92ad-deff6af18ba9')
s = json.dumps(n, ensure_ascii=False, indent=2)
# 输出 5000-6998 字符
print(s[5000:])