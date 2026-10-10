import connect_db

from flask import Flask, render_template
import zoneinfo

app = Flask(__name__)

@app.route('/')
def index():
    with connect_db.connect_to_db() as connection:
        conferences = connect_db.get_conferences_info(connection)

    return render_template('index.html', conferences=conferences)

@app.template_filter()
def jst_format(value):
    if value is None:
        return "未取得"
    return value.astimezone(zoneinfo.ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter()
def date_format(start_date, end_date):
    if start_date is None or end_date is None:
        return "未取得"
    
    start_date_str = f'{start_date.year}年{start_date.month}月{start_date.day}日'

    if start_date == end_date:
        return start_date_str

    if start_date.year != end_date.year:
        end_date_str = f'{end_date.year}年{end_date.month}月{end_date.day}日'
    elif start_date.month != end_date.month:
        end_date_str = f'{end_date.month}月{end_date.day}日'
    else:
        end_date_str = f'{end_date.day}日'

    return f"{start_date_str} ~ {end_date_str}"

if __name__ == '__main__':
    app.run(debug=True)