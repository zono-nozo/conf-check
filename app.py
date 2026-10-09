import connect_db

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    with connect_db.connect_to_db() as connection:
        rows = connect_db.get_conferences_info(connection)

    return str(rows)

if __name__ == '__main__':
    app.run(debug=True)