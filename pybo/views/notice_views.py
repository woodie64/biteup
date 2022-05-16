import os
from datetime import datetime
from pybo.views.auth_views import login_required
from flask import Blueprint, render_template, request, url_for, g, flash, send_file
from werkzeug.utils import secure_filename

from .. import db
from ..forms import NoticeForm, AnoticeForm
from ..models import Notice, Anotice, User

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'pybo\\static\\upload_file\\notice')
bp = Blueprint('notice', __name__, url_prefix='/notice')

file_path = "templates/upload_file/"


@bp.route('/list')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    # 조회
    notice_list = Notice.query.order_by(Notice.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Anotice.notice_id, Anotice.content, User.username) \
            .join(User, Anotice.user_id == User.id).subquery()
        notice_list = notice_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.notice_id == Notice.id) \
            .filter(Notice.subject.ilike(search) |  # 제목
                    Notice.content.ilike(search) |  # 내용
                    User.username.ilike(search) |  # 작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    notice_list = notice_list.paginate(page, per_page=10)
    return render_template('notice/notice_list.html', notice_list=notice_list, page=page, kw=kw)


@bp.route('/detail/<int:notice_id>/')
def detail(notice_id):
    form = AnoticeForm()
    notice = Notice.query.get_or_404(notice_id)
    return render_template('notice/notice_detail.html', notice=notice, form=form)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if g.user.email == "biteup@biteup.com":
        print("/create")
        form = NoticeForm()
        filename = None
        if request.method == 'POST' and form.validate_on_submit():
            if request.files['file']:
                filename = file_upload(request.files['file'])

            notice = Notice(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                                user=g.user, file=filename)
            db.session.add(notice)
            db.session.commit()
            return '<script>alert("작성되었습니다.");location.href="/notice/list"</script>'
        return render_template('notice/notice_form.html', form=form)
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/modify/<int:notice_id>', methods=('GET', 'POST'))
@login_required
def modify(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    if g.user != notice.user:
        return '<script>alert("수정 권한이 없습니다.");location.href="/notice/detail/' + str(notice_id) + '"</script>'
        # return redirect(url_for('notice.detail', notice_id=notice_id))
    if request.method == 'POST':  # POST 요청
        form = NoticeForm()
        if form.validate_on_submit():
            if request.files['file']:
                filename = file_upload(request.files['file'])
                notice.file = filename

            notice.content = form.content.data
            notice.subject = form.subject.data
            notice.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            # return redirect(url_for('notice.detail', notice_id=notice_id))
            return '<script>alert("수정되었습니다.");location.href="/notice/detail/' + str(notice_id) + '"</script>'
    else:  # GET 요청
        form = NoticeForm(obj=notice)
    return render_template('notice/notice_form.html', form=form)


@bp.route('/delete/<int:notice_id>')
@login_required
def delete(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    if g.user != notice.user:
        return '<script>alert("삭제 권한이 없습니다.");location.href="/notice/detail/' + str(notice_id) + '"</script>'
    db.session.delete(notice)
    db.session.commit()
    # return redirect(url_for('notice._list'))
    return '<script>alert("삭제되었습니다.");location.href="/notice/list"</script>'


@bp.route('/file_download/<string:file_name>')
@login_required
def file_download(file_name):
    print("file_download success")
    try:
        path = os.getcwd()
        UPLOAD_FOLDER = os.path.join(path, 'pybo\\static\\upload_file\\\\notice')
        file_name = UPLOAD_FOLDER + file_name
        print(file_name)
    except:
        return '<script>alert("error");</script>'
    return send_file(file_name, mimetype='image/png', as_attachment=True)


def file_upload(file):
    print("file_upload")
    filename = secure_filename(file.filename)
    file.save(UPLOAD_FOLDER + "\\" + filename)
    return filename
