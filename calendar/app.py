import calendar
import jpholiday
from datetime import datetime
from jinja2 import Template
import os
import zipfile
from flask import Flask, send_file

app = Flask(__name__)

# カレンダーのひな形HTMLファイルを読み込む関数
def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_holidays(year):
    holidays = {}
    for date, name in jpholiday.year_holidays(year):
        holidays[(date.year, date.month, date.day)] = name
    return holidays

def create_monthly_calendar(year, month, template, holidays):
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 祝日情報の追加
    month_calendar = []
    for week in month_days:
        week_with_holidays = []
        for day in week:
            is_holiday = (year, month, day) in holidays if day != 0 else False
            week_with_holidays.append((day, is_holiday))
        month_calendar.append(week_with_holidays)

    template = Template(template)
    rendered_html = template.render(year=year, month=month, calendar=month_calendar, holidays=holidays)
    return rendered_html

def save_calendars_to_zip(year, template_path, output_zip):
    template = load_template(template_path)
    holidays = get_holidays(year)
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for month in range(1, 13):
            calendar_html = create_monthly_calendar(year, month, template, holidays)
            filename = f"{str(year)[2:]}_{month:02}.html"  # ファイル名の形式を修正
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(calendar_html)
            zipf.write(filename)
            os.remove(filename)

# 現在の年を取得し、翌年のカレンダーを生成
current_year = datetime.now().year
next_year = current_year + 1
template_path = 'calendar_template.html'
output_zip = f'calendars_{next_year}.zip'
save_calendars_to_zip(next_year, template_path, output_zip)

@app.route('/download')
def download_file():
    return send_file(output_zip, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
