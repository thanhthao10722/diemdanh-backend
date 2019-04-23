from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rollcall.auth import login_required
from rollcall.db import get_db
from flask import jsonify

bp = Blueprint('Fingerprint', __name__)

#đăng ký theo ID vân tay
@bp.route('/transfer/<data>',methods=('GET', 'POST'))
def transfer(data):
    if request.method == 'POST':
        MSSV= request.form['MSSV']

        db = get_db()
        error = None

        if not MSSV:
            error = 'MSSV is required.'
        elif db.execute(
            'SELECT MSSV FROM Student WHERE MSSV = ?',(MSSV,)
        ).fetchone() is None:
            error = 'MSSV doesnt {} exist'.format(MSSV)

        if error is None:
            db.execute(
                'INSERT INTO FingerPrint VALUES (?, ?)',
                (data,MSSV)
            )
            db.commit()
            return redirect(url_for('course.index'))
        flash(error)
    return render_template('course/createID.html')


#check vân tay thực hiện điểm danh
@bp.route('/check/<data>')
def check(data):
    db= get_db()
    MaHocPhan = 1
    TinhTrang = 'Đã Điểm Danh'
    
    SV = db.execute(
        'SELECT * FROM Class '
        'WHERE MSSV = (SELECT MSSV FROM FingerPrint WHERE FingerPrintId = ?) ',
        (data,)
    ).fetchone() 

    if SV is not None:
        db.execute(
           'UPDATE RollCall '
           'SET Status = ? '
           'WHERE IDSC = ? AND MSSV = (SELECT MSSV FROM FingerPrint WHERE FingerPrintId = ?) ',(TinhTrang, MaHocPhan, data)
        )
        db.commit()
        
        return jsonify(MaVanTay=data)
        
    if SV is None: 
        return render_template('course/Uncheck.html')