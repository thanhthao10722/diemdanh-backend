from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT sv.MSSV, sv.HoTen, dk.MaHocPhan, MonHoc, HocKy, DiemDanh '
        'FROM SinhVien sv JOIN DangKy dk ON sv.MSSV=dk.MSSV'
        'JOIN HocPhan ON HocPhan.MaHocPhan = dk.MaHocPhan'
        'ORDER BY HoTen DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


def get_post(MSSV, check_author=True):
    post = get_db().execute(
        'SELECT sv.MSSV, sv.HoTen, dk.MaHocPhan, MonHoc, HocKy, DiemDanh '
        'FROM SinhVien sv JOIN DangKy dk ON sv.MSSV=dk.MSSV'
        'JOIN HocPhan ON HocPhan.MaHocPhan = dk.MaHocPhan'
        'WHERE sv.MSSV = ?',
        (MSSV,)
        
    ).fetchone()

    return post








