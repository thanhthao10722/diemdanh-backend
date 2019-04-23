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
    for i  in list:
            get_db().execute(
                'INSERT INTO RollCall(IDSC, MSSV, Status, Note) VALUES(?, ?, ?, ?)',
                (i['IDSC'],i['MSSV'],'Chưa Điểm Danh','')
            )
            get_db().commit()         
    return redirect(url_for('DiemDanh.HocPhan',IDSC = IDSC))


@bp.route('/<IDSC>/HocPhan', methods=('GET', 'POST'))
def HocPhan(IDSC):
    posts = get_db().execute(
        'SELECT * FROM Class INNER JOIN Student on Class.MSSV = Student.MSSV '
        'INNER JOIN RegisteredCourse on RegisteredCourse.IDRCourse = Class.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        'INNER JOIN ScheduledCourse on ScheduledCourse.IDRCourse = RegisteredCourse.IDRCourse '
        'INNER JOIN RollCall on RollCall.IDSC = ScheduledCourse.IDSC '
        'WHERE RollCall.IDSC = ? '
        'ORDER BY FullName ',(IDSC),
    ).fetchall()
    return render_template('course/CSDL.html',posts = posts)

def get_post(MSSV,IDSC):
    post = get_db().execute(
        'SELECT * FROM Class INNER JOIN Student on Class.MSSV = Student.MSSV '
        'INNER JOIN RegisterdCourse on RegisterdCourse.IDRCourse = Class.IDRCourse '
        'INNER JOIN Course on Course.IDCourse = RegisteredCourse.IDCourse '
        'INNER JOIN ScheduledCourse on ScheduledCourse.IDRCourse = RegisterdCourse.IDRCourse '
        'INNER JOIN RollCall on RollCall.IDSC = ScheduledCourse.IDSC '
        'ORDER BY FullName WHERE RollCall.IDSC = ? AND MSSV = ? ',(IDSC,MSSV),
    ).fetchone()
    return post