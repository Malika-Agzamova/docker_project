from flask import Flask, render_template, request
import pg8000


app = Flask(__name__, template_folder='templates')


def get_data_from_db(query):
    conn = pg8000.connect(user='malika', password='strong_pass', host='localhost', database='malika', port=5432)
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        level = request.form['level']
        return render_template('timetable.html', level=level)

    all_levels = get_data_from_db("SELECT DISTINCT level FROM timetable order by level;")
    all_students = get_data_from_db("SELECT * FROM student;")

    return render_template('index.html', levels=all_levels, students=all_students)


@app.route('/timetable', methods=['GET'])
def timetable():
    level = request.args.get('level')
    conn = pg8000.connect(user='malika', password='strong_pass', host='localhost', database='malika', port=5432)
    cur = conn.cursor()

    if level == 'all':
        query = "SELECT * FROM timetable;"
    else:
        query = f"SELECT * FROM timetable WHERE level = {level};"
    timetables = get_data_from_db(query)
    print(timetables)

    message = "No timetable found for this level" if not timetables else None
    return render_template('timetable.html', data=timetables, message=message, level=level)


if __name__ == '__main__':
    app.run(debug=True)
