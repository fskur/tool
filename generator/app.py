import calendar
import json
import os
import uuid
from flask import Flask, render_template, request, session, jsonify, send_from_directory
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# セッションキーの暗号化キーを設定
app.secret_key = 'your_secret_key_here'

# ユーザーIDをセットアップする関数
def setup_user():
    if 'user_id' not in session:
        # ユーザーIDがセッションにない場合、新しいユーザーIDを生成
        session['user_id'] = generate_user_id()
    return session['user_id']

# 全てのリクエストの前にユーザーIDをセットアップ
@app.before_request
def before_request():
    setup_user()

def generate_user_id():
    # ユーザーIDをUUID形式で生成
    return str(uuid.uuid4())

# テンプレート読み込み
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('calendar.j2')

# ユーザーホームディレクトリのパスを取得
user_home = os.path.expanduser("~")

def generate_calendar_data(selected_year, selected_month, request_data):
    # 月初の週の日付を計算
    first_week_day = (calendar.weekday(selected_year, selected_month, 1) + 1) % 7
    start_day = 1 - first_week_day

    # 月の日数を取得
    days_in_month = calendar.monthrange(selected_year, selected_month)[1]

    # カレンダーデータを初期化
    calendar_data = {
        "month": selected_month,
        "class": []
    }

    # 月初の週からデータを生成
    for day in range(start_day, days_in_month + 1):
        if day <= 0:
            mmdd = ""  # 日付が0以下の場合は空欄
        else:
            mmdd = f"{selected_month:02d}{day:02d}"  # 月と日をmmdd形式に変換

        day_data = {
            "day": day if day > 0 else "",  # 日付が0以下の場合は空欄
            "day_link": mmdd,
            "time_am": request_data.get(f"day_{day}", {}).get("time_am", ""),
            "menu_am": request_data.get(f"day_{day}", {}).get("menu_am", ""),
            "teacher_am": request_data.get(f"day_{day}", {}).get("teacher_am", ""),
            "price_am": request_data.get(f"day_{day}", {}).get("price_am", ""),
            "time_pm": request_data.get(f"day_{day}", {}).get("time_pm", ""),
            "menu_pm": request_data.get(f"day_{day}", {}).get("menu_pm", ""),
            "teacher_pm": request_data.get(f"day_{day}", {}).get("teacher_pm", ""),
            "price_pm": request_data.get(f"day_{day}", {}).get("price_pm", "")
        }
        calendar_data["class"].append(day_data)

    # 最終週まで空欄を追加
    last_week_day = (calendar.weekday(selected_year, selected_month, days_in_month) + 1) % 7
    end_day = 7 - last_week_day - 1
    for day in range(1, end_day + 1):
        day_data = {
            "day": "",  # 日付が0以下の場合は空欄
            "day_link": "",  # 日付が0以下の場合は空欄
            "time_am": "",
            "menu_am": "",
            "teacher_am": "",
            "price_am": "",
            "time_pm": "",
            "menu_pm": "",
            "teacher_pm": "",
            "price_pm": ""
        }
        calendar_data["class"].append(day_data)

    return calendar_data

@app.route('/run_script', methods=['POST'])
def run_script():
    selected_year = int(request.json['year'])
    selected_month = int(request.json['month'])

    calendar_data = generate_calendar_data(selected_year, selected_month, request.json)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(calendar_data, file, indent=2, ensure_ascii=False)
    return jsonify({"message": "JSONデータができたよ！"})

@app.route('/run_rendering', methods=['POST'])
def run_rendering():
    try:
        # 設定ファイル読み込み
        with open('data.json', 'r', encoding='utf-8') as f:
            calendar_data = json.load(f)

        # calendar_data リストが空でない場合のみ処理を実行
        if calendar_data:
            # レンダリングしてhtml出力
            rendered_html = tmpl.render(class_info=calendar_data)

            # result.htmlをアプリケーションのディレクトリに保存
            file_path = os.path.join(os.getcwd(), "result.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                # ファイルに書き込む
                f.write(rendered_html)

            return jsonify({"message": "htmlができたよ！"})
        else:
            # エラーメッセージや代替の処理を行う
            return jsonify({"error": "calendar_data リストが空っぽ"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/tool/generator/cooking.html')
def cooking_page():
    return render_template('cooking.html')

@app.route('/tool/generator/result.html')
def get_result_html():
    return send_from_directory(os.path.expanduser("~/tool/generator/"), 'result.html')

if __name__ == '__main__':
    app.run()
