from datetime import datetime
from pybo.views.auth_views import login_required
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import NoticeForm, AnoticeForm
from ..models import Notice, Anotice, User

bp = Blueprint('notice', __name__, url_prefix='/notice')


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    # 조회
    notice_list = Notice.query.order_by(Notice.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(AnoticeForm.notice_id, AnoticeForm.content, User.username) \
            .join(User, AnoticeForm.user_id == User.id).subquery()
        notice_list = notice_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.notice_id == Notice.id) \
            .filter(Notice.subject.ilike(search) |  # 질문제목
                    Notice.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
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


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = NoticeForm()
    if request.method == 'POST' and form.validate_on_submit():
        notice = Notice(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(notice)
        db.session.commit()
        # return redirect(url_for('notice._list'))
        return '<script>alert("생성되었습니다.");location.href="/notice/list"</script>'
    return render_template('notice/notice_form.html', form=form)


@bp.route('/modify/<int:notice_id>', methods=('GET', 'POST'))
@login_required
def modify(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    if g.user != notice.user:
        return '<script>alert("수정 권한이 없습니다.");location.href=/profile/</script>'
        # return redirect(url_for('notice.detail', notice_id=notice_id))
    if request.method == 'POST':  # POST 요청
        form = NoticeForm()
        if form.validate_on_submit():
            form.populate_obj(notice)
            notice.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            # return redirect(url_for('notice.detail', notice_id=notice_id))
            return '<script>alert("수정되었습니다.");location.href=/notice/detail</script>'
    else:  # GET 요청
        form = NoticeForm(obj=notice)
    return render_template('notice/notice_form.html', form=form)


@bp.route('/delete/<int:notice_id>')
@login_required
def delete(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    if g.user != notice.user:
        flash('삭제권한이 없습니다')
        return '<script>alert("삭제 권한이 없습니다.");location.href=/notice/detail</script>'
        # return redirect(url_for('notice.detail', notice_id=notice_id))
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for('notice._list'))