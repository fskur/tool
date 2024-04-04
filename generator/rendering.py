from jinja2 import Template, Environment, FileSystemLoader
import json

#テンプレート読み込み
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('calendar.j2')

#設定ファイル読み込み
with open('data.json', 'r', encoding='utf-8') as f:
    params = json.load(f)

# JSONデータを出力して確認
print(params)

#レンダリングしてhtml出力
rendered_html = tmpl.render(params)
with open('result.html', 'w') as f:
    f.write(rendered_html)