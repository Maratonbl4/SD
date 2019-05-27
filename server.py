from flask import Flask, render_template, request
import pymysql.cursors
from flask import jsonify

connection = pymysql.connect(host='localhost', # а тут можешь не менять в общем то ничего, это адресс sql сервера в сети, но раз ты юзаешь комп как сервер и sql то забей
                             user='marat',  # тут введи имя пользователя бд
                             password='123',  # а тут введи его пароль
                             db='diplom',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'form': {
            'geometry': set(),
            'back_angle': set(),
            'tolerance': set(),
            'hole_type': set()
        },
        'grade': {
            'name': set(),
            'material': set(),
            'speed': set()
        },
        'chipbreaker': {
            'name': set(),
            'material': set(),
            'speed': set()
        },
        'dimensions': {
            'length': set(),
            'thikness': set(),
            'radius': set(),
        }
    }
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM form;')
        for a in cursor.fetchall():
            context['form']['geometry'].add(a['GeometryRus'])
            context['form']['back_angle'].add(a['BackAngleRus'])
            context['form']['tolerance'].add(a['ToleranceRus'])
            context['form']['hole_type'].add(a['holeTypeRus'])

        cursor.execute('SELECT * FROM dimensions;')
        for a in cursor.fetchall():
            context['dimensions']['length'].add(a['Length'])
            context['dimensions']['thikness'].add(a['Thikness'])
            context['dimensions']['radius'].add(a['Radius'])

        cursor.execute('SELECT * FROM grade;')
        for a in cursor.fetchall():
            context['grade']['material'].add(a['MaterialRus'])
            context['grade']['speed'].add(a['SpeedRus'])

        cursor.execute('SELECT * FROM chipbreaker;')
        for a in cursor.fetchall():
            context['chipbreaker']['material'].add(a['MaterialRus'])
            context['chipbreaker']['speed'].add(a['SpeedRus'])

    return render_template('index.html', **context)


@app.route('/get_carbide_plate', methods=['post'])
def get_carbide_plate():
    data = request.json['parametrs']

    # form
    results = []
    with connection.cursor() as cursor1:
        cursor1.execute(
            f'SELECT Geometry, BackAngle, Tolerance, HoleType FROM form WHERE GeometryRus="{data["f_g"]}" and BackAngleRus="{data["f_b"]}" and ToleranceRus="{data["f_t"]}" and holeTypeRus="{data["f_h"]}";')
        form = cursor1.fetchall()

    # dimensions
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT Length, Thikness, Radius FROM dimensions WHERE Length="{data["d_l"]}" and Thikness="{data["d_t"]}" and Radius="{data["d_r"]}";')
        dimensions = cursor.fetchall()

    # chipbreaker
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT Name FROM chipbreaker WHERE MaterialRus="{data["c_m"]}" and SpeedRus="{data["c_s"]}";')
        chipbreaker = cursor.fetchall()

    # grade
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT Name FROM grade WHERE MaterialRus="{data["g_m"]}" and SpeedRus="{data["g_s"]}";')
        grade = cursor.fetchall()

    for f in form:
        for d in dimensions:
            for c in chipbreaker:
                for g in grade:
                    results.append(
                        f'{"".join(f.values())}-{"".join(d.values())}-{"".join(c.values())}-{"".join(g.values())}')

    if not len(results):
        return jsonify({'results': ['пластины с такой конфигурацией отсутствуют, попробуйте другой вариант']})
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run()
