import datetime
import calendar
import json
import subprocess
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

    print("JSONデータをファイルに書き込みました。")
    return jsonify(calendar_data)

@app.route('/run_rendering', methods=['POST'])
def run_rendering():
    try:
        python_executable = sys.executable
        subprocess.run([python_executable, 'rendering.py'], check=True)
        return jsonify({"message": "Rendering script executed successfully"})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Error executing rendering script"})

@app.route('/tool/generator/cooking.html')
def cooking_page():
    return render_template('cooking.html')

if __name__ == '__main__':
    app.run(port=8000)
