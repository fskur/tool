from jinja2 import Environment, FileSystemLoader
import json

# テンプレート読み込み
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('calendar.j2')

# 設定ファイル読み込み
with open('data.json', 'r', encoding='utf-8') as f:
    class_data = json.load(f)

# レンダリングしてhtml出力
rendered_html = tmpl.render(class_info=class_data[0])
with open('result.html', 'w') as f:
    f.write(rendered_html)
