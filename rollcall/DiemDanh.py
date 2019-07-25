from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rollcall.auth import login_required
from rollcall.db import get_db
from flask import jsonify

bp = Blueprint('DiemDanh', __name__)

#xuất thông tin sinh viên lớp học phần cơ sở dữ liệu
@bp.route('/<IDSC>/DiemDanh', methods=('GET', 'POST'))
def DiemDanh(IDSC):
    IDSC = IDSC
    list = get_db().execute('SELECT * FROM Class INNER JOIN Student on Class.MSSV = Student.MSSV '
        'INNER JOIN RegisteredCourse on RegisteredCourse.IDRCourse = Class.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        'INNER JOIN ScheduledCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'WHERE IDSC = ? '
        'ORDER BY FullName ',(IDSC),).fetchall()

    for i in list:
        SV = get_db().execute(
            'SELECT * FROM RollCall WHERE MSSV = ? AND IDSC = ?',(i['MSSV'],i['IDSC']),
        ).fetchone()
        if SV is None:
            get_db().execute(
                'INSERT INTO RollCall(IDSC, MSSV, Status, Note) VALUES(?, ?, ?, ?)',
                (i['IDSC'],i['MSSV'],'Chưa Điểm Danh','')
            )
            flash("abc")
            get_db().commit()         
    return redirect(url_for('DiemDanh.HocPhan',IDSC = IDSC))
            

@bp.route('/<IDSC>/HocPhan', methods=('GET', 'POST'))
def HocPhan(IDSC):
    posts = get_db().execute(
        'SELECT * FROM RollCall INNER JOIN Student on RollCall.MSSV = Student.MSSV '
        'INNER JOIN ScheduledCourse on RollCall.IDSC = ScheduledCourse.IDSC '
        'INNER JOIN RegisteredCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        'WHERE RollCall.IDSC = ? '
        ,(IDSC),
    ).fetchall()
    return render_template('course/CSDL.html',posts = posts)

def get_post(MSSV,IDSC):
    post = get_db().execute(
        'SELECT * FROM RollCall INNER JOIN Student on RollCall.MSSV = Student.MSSV '
        'INNER JOIN ScheduledCourse on RollCall.IDSC = ScheduledCourse.IDSC '
        'INNER JOIN RegisteredCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        ' WHERE RollCall.IDSC = ? AND MSSV = ? ',(IDSC,MSSV),
    ).fetchone()
    return post