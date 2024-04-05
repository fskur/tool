import datetime
import calendar
import json
import subprocess
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_calendar_data(selected_year, selected_month, request_data):
    days_in_month = calendar.monthrange(selected_year, selected_month)[1]
    calendar_data = {
        "month": selected_month,
        "class": []
    }
    for day in range(1, days_in_month + 1):
        mmdd = f"{selected_month:02d}{day:02d}"  # 月と日をmmdd形式に変換
        day_data = {
            "day": day,
            "day_link": mmdd,
            "time_am": request_data.get(f"day_{day}", {}).get("time_am", ""), # 初期値を空に設定
            "menu_am": request_data.get(f"day_{day}", {}).get("menu_am", ""), # 初期値を空に設定
            "teacher_am": request_data.get(f"day_{day}", {}).get("teacher_am", ""), # 初期値を空に設定
            "price_am": request_data.get(f"day_{day}", {}).get("price_am", ""), # 初期値を空に設定
            "time_pm": request_data.get(f"day_{day}", {}).get("time_pm", ""), # 初期値を空に設定
            "menu_pm": request_data.get(f"day_{day}", {}).get("menu_pm", ""), # 初期値を空に設定
            "teacher_pm": request_data.get(f"day_{day}", {}).get("teacher_pm", ""), # 初期値を空に設定
            "price_pm": request_data.get(f"day_{day}", {}).get("price_pm", "")  # 初期値を空に設定
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
