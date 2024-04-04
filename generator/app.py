import datetime
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_calendar_data(selected_year, selected_month):
    starting_day = datetime.datetime(selected_year, selected_month, 1).weekday()
    days_in_month = (datetime.datetime(selected_year, selected_month % 12 + 1, 1) - datetime.datetime(selected_year, selected_month, 1)).days

    calendar_data = []

    for day in range(1, days_in_month + 1):
        day_data = {
          "month": selected_month,
          "class": [
            { "day": day,
              "time_am": request.json[f"day_{day}"]["time_am"], # 初期値を空に設定
              "menu_am": request.json[f"day_{day}"]["menu_am"], # 初期値を空に設定
              "teacher_am": request.json[f"day_{day}"]["teacher_am"], # 初期値を空に設定
              "price_am": request.json[f"day_{day}"]["price_am"], # 初期値を空に設定
              "time_pm": request.json[f"day_{day}"]["time_pm"], # 初期値を空に設定
              "menu_pm": request.json[f"day_{day}"]["menu_pm"], # 初期値を空に設定
              "teacher_pm": request.json[f"day_{day}"]["teacher_pm"], # 初期値を空に設定
              "price_pm": request.json[f"day_{day}"]["price_pm"]  # 初期値を空に設定
            }
          ]
        }
        calendar_data.append(day_data)

    return calendar_data

@app.route('/run_script', methods=['POST'])
def run_script():
    selected_year = int(request.json['year'])
    selected_month = int(request.json['month'])

    calendar_data = generate_calendar_data(selected_year, selected_month)

    with open("data.json", "w") as file:
        json.dump(calendar_data, file, indent=2, ensure_ascii=False)

    print("JSONデータをファイルに書き込みました。")
    return jsonify(calendar_data)

@app.route('/tool/generator/cooking.html')
def cooking_page():
    return render_template('cooking.html')

if __name__ == '__main__':
    app.run(port=8000)