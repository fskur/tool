from jinja2 import Environment, FileSystemLoader
import json
from app import app

# テンプレート読み込み
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('calendar.j2')

# 設定ファイル読み込み
with open('data.json', 'r', encoding='utf-8') as f:
    calendar_data = json.load(f)

# calendar_data リストが空でない場合のみ処理を実行
if calendar_data:
    # レンダリングしてhtml出力
    rendered_html = tmpl.render(class_info=calendar_data)
    with open('result.html', 'w') as f:
        f.write(rendered_html)
else:
    # エラーメッセージや代替の処理を行う
    print("calendar_data リストが空です。")

# Flaskアプリケーションを実行
if __name__ == '__main__':
    app.run(port=8001)
