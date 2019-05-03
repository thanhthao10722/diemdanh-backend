from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rollcall.auth import login_required
from rollcall.db import get_db
from flask import jsonify

bp = Blueprint('course', __name__)

#trang chu
@login_required
@bp.route('/') 
def index():
    return render_template('course/index.html')


#đăng ký theo mã học phần
@bp.route('/create', methods=('GET', 'POST'))
def create():
     if request.method == 'POST':
        MSSV= request.form['MSSV']
        MaHocPhan = request.form['MaHocPhan']
       
        db = get_db()
       
        error = None

        if not MSSV:
            error = 'MSSV is required.'
        elif not MaHocPhan:
            error = 'MaHocPhan is required.'
        elif db.execute(
            'SELECT MSSV FROM Student WHERE MSSV = ?', (MSSV,)
        ).fetchone() is None:
            error = 'MSSV {} doesnt exist'.format(MSSV)
        elif db.execute(
            'SELECT IDCourse FROM Course WHERE IDCourse = ?', (MaHocPhan,)
        ).fetchone() is None:
            error = 'MaHocPhan{} doesnt exist'.format(MaHocPhan)
        if error is None:
            IDRCourse = db.execute(
                'SELECT IDRCourse FROM RegisteredCourse WHERE IDCourse = ?',
                (MaHocPhan,)
            ).fetchone()

            db.execute(
                'INSERT INTO Class(MSSV, IDRCourse) VALUES (?, ?)',
                (MSSV, IDRCourse['IDRCourse'])
            )
            db.commit()
            return redirect(url_for('course.index'))
        flash(error)

     return render_template('course/create.html')

      
@bp.route('/<MSSV>/<IDSC>/delete', methods=('POST','GET'))
def delete(MSSV,IDSC):
    db = get_db()
    db.execute('DELETE FROM Class WHERE MSSV = ?', (MSSV,))
    db.commit()
    db.execute('DELETE FROM RollCall WHERE MSSV = ?', (MSSV,))
    db.commit()
    return redirect(url_for('DiemDanh.HocPhan',IDSC = IDSC))


def get_class(IDSC):
    course = get_db().execute(
        'SELECT * FROM ScheduledCourse INNER JOIN RegisteredCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        ' WHERE IDRCouse = ? '
        'ORDER BY Room',(IDSC),
    ).fetchone()
    return course

#show ra phòng học
@bp.route('/show', methods=('POST','GET'))
def show():
    courses = get_db().execute(
        'SELECT * FROM ScheduledCourse INNER JOIN RegisteredCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        'ORDER BY Room',
    ).fetchall()
    return render_template('course/show.html',courses = courses)
