from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

#trang chu
@login_required
@bp.route('/') 
def index():
    return render_template('blog/index.html')


#Form dang ky theo học phần
#đăng ký theo mã học phần
@bp.route('/create', methods=('GET', 'POST'))
def create():
     if request.method == 'POST':
        MSSV= request.form['MSSV']
        MaHocPhan = request.form['MaHocPhan']
        TinhTrang ='Chưa Điểm Danh'
        db = get_db()
       
        error = None

        if not MSSV:
            error = 'MSSV is required.'
        elif not MaHocPhan:
            error = 'MaHocPhan is required.'
        elif db.execute(
            'SELECT MSSV FROM SinhVien WHERE MSSV = ?', (MSSV,)
        ).fetchone() is None:
            error = 'MSSV {} doesnt exist'.format(MSSV)
        elif db.execute(
            'SELECT MaHocPhan FROM HocPhan WHERE MaHocPhan = ?', (MaHocPhan,)
        ).fetchone() is None:
            error = 'MaHocPhan{} doesnt exist'.format(MaHocPhan)
        if error is None:
            db.execute(
                'INSERT INTO DangKy(MSSV, MaHocPhan, TinhTrang) VALUES (?, ?, ?)',
                (MSSV, MaHocPhan, TinhTrang)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        flash(error)

     return render_template('blog/create.html')


#đăng ký theo ID vân tay
@bp.route('/transfer/<data>',methods=('GET', 'POST'))
def transfer(data):
    if request.method == 'POST':
        MSSV= request.form['MSSV']
        HoTen = request.form['HoTen']
        db = get_db()
       
        error = None

        if not MSSV:
            error = 'MSSV is required.'
        elif not HoTen:
            error = 'HoTen is required.'
        elif db.execute(
            'SELECT MSSV FROM SinhVien WHERE MSSV = ?', (MSSV,)
        ).fetchone() is not None:
            error = 'MSSV {} exist'.format(MSSV)

        if error is None:
            db.execute(
                'INSERT INTO SinhVien(IDTay, MSSV, HoTen) VALUES (?, ?, ?)',
                (data, MSSV, HoTen)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('blog/createID.html')

#xuất thông tin sinh viên lớp học phần cơ sở dữ liệu
@bp.route('/CSDL', methods=('GET', 'POST'))
def CSDL():
    MaHocPhan = 'MH1'
    TinhTrang = 'Chưa Điểm Danh'

    db = get_db()
    posts = db.execute(
        'SELECT sv.MSSV, sv.HoTen, dk.MaHocPhan, MonHoc, HocKy, TinhTrang, SoBuoiVang '
        'FROM SinhVien sv JOIN DangKy dk ON sv.MSSV=dk.MSSV '
        'JOIN HocPhan ON HocPhan.MaHocPhan = dk.MaHocPhan '
        'WHERE dk.MaHocPhan = "MH1" '
        'ORDER BY HoTen ASC '
    ).fetchall()
    return render_template('blog/CSDL.html',posts=posts)

def get_post(MSSV, check_author=True):
    post = get_db().execute(
        'SELECT sv.MSSV, sv.HoTen, dk.MaHocPhan, MonHoc, HocKy, TinhTrang, SoBuoiVang '
        'FROM SinhVien sv JOIN DangKy dk ON sv.MSSV=dk.MSSV '
        'JOIN HocPhan ON HocPhan.MaHocPhan = dk.MaHocPhan '
        'WHERE dk.MaHocPhan = "MH1" '
        'AND sv.MSSV = ?',
        (MSSV,)
    ).fetchone()

    return post

#check vân tay thực hiện điểm danh
@bp.route('/check/<data>')
def check(data):
    db= get_db()
    MaHocPhan = 'MH1'
    TinhTrang = 'Đã Điểm Danh'

    SV = db.execute(
        'SELECT * FROM SinhVien sv JOIN DangKy dk on sv.MSSV =dk.MSSV '
        'WHERE dk.MaHocPhan = ? AND IDTay = ?',
        (MaHocPhan, data, )
    ).fetchone() 
    
    if SV is not None:
        db.execute(
           'UPDATE DangKy '
           'SET TinhTrang = ? '
           'WHERE MaHocPhan = ? AND MSSV = (SELECT MSSV FROM SinhVien WHERE IDTay = ?) ',(TinhTrang, MaHocPhan, data,)
        )
        db.commit()
        return render_template('blog/Check.html')
    if SV is None: 
        return render_template('blog/Uncheck.html')

        

@bp.route('/<MSSV>/delete', methods=('POST','GET'))
def delete(MSSV):
    get_post(MSSV)
    db = get_db()
    db.execute('DELETE FROM DangKy WHERE MSSV = ?', (MSSV,))
    db.commit()
    return redirect(url_for('blog.CSDL'))



@bp.route('/complete', methods=('POST','GET'))
def complete():

    MaHocPhan = 'MH1'
    TinhTrang = 'Chưa Điểm Danh'
    db = get_db()
    db.execute(
        'UPDATE DangKy SET SoBuoiVang = SoBuoiVang+1 '
        ' WHERE MaHocPhan = ? AND TinhTrang = ? ',
        (MaHocPhan, TinhTrang)
    )
    db.commit()
     
    return redirect(url_for('blog.CSDL'))

@bp.route('/reset', methods=('POST','GET'))
def reset():

    MaHocPhan = 'MH1'
    TinhTrang = 'Chưa Điểm Danh'
    db = get_db()
    
    #set lại tình trạng chưa điểm danh cho lần điểm danh tới
    db.execute(
        'UPDATE DangKy SET TinhTrang = ? '
        ' WHERE MaHocPhan = ? ',
        (TinhTrang, MaHocPhan)
    )
    db.commit()
    return redirect(url_for('blog.CSDL'))


