import connect_db

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    with connect_db.connect_to_db() as connection:
        conferences = connect_db.get_conferences_info(connection)

    return render_template('index.html', conferences=conferences)

if __name__ == '__main__':
    app.run(debug=True)