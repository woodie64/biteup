from flask import Blueprint, render_template

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def admin():
    return render_template('admin/admin_form.html')


@bp.route('/list/')
def _list():
    return render_template('admin/admin_list.html')
