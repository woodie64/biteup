import os
from datetime import datetime, date, timedelta
from pybo.views.auth_views import login_required
from flask import Blueprint, render_template, request, url_for, g, flash, send_file
from werkzeug.utils import secure_filename

from .. import db
from ..forms import CommunityForm, AnswerForm
from ..models import Community, Answer, User

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'pybo\\static\\upload_file')
bp = Blueprint('community', __name__, url_prefix='/community')

file_path = "templates/upload_file/"


@bp.route('/list')
@login_required
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    # 조회
    community_list = Community.query.order_by(Community.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.community_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        community_list = community_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.community_id == Community.id) \
            .filter(Community.subject.ilike(search) |  # 제목
                    Community.content.ilike(search) |  # 내용
                    User.username.ilike(search) |  # 작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    community_list = community_list.paginate(page, per_page=10)
    return render_template('community/community_list.html', community_list=community_list, page=page, kw=kw)


@bp.route('/detail/<int:community_id>/')
@login_required
def detail(community_id):
    form = AnswerForm()
    community = Community.query.get_or_404(community_id)

    #조회수 증가
    community.hits = community.hits + 1
    db.session.commit()

    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    # 조회
    community_list = Community.query.order_by(Community.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.community_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        community_list = community_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.community_id == Community.id) \
            .filter(Community.subject.ilike(search) |  # 제목
                    Community.content.ilike(search) |  # 내용
                    User.username.ilike(search) |  # 작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    # 페이징
    community_list = community_list.paginate(page, per_page=10)
    return render_template('community/community_detail.html', community=community, form=form, community_list=community_list, page=page, kw=kw)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CommunityForm()
    filename = None

    if request.method == 'POST' and form.validate_on_submit():
        if request.files['file']:
            filename = file_upload(request.files['file'])

        community = Community(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                              user=g.user, file=filename, hits=1)

        db.session.add(community)
        db.session.commit()

        #로그
        print("게시글 생성")
        print("작성자 : " + g.user.email)
        print("별명 : " + g.user.username)
        print("제목 : " + form.subject.data)
        print("내용 : "+ form.content.data)
        if filename is not None:
            print("업로드 파일 : "+ filename)
        ###
        return '<script>alert("작성 되었습니다.");location.href="/community/list"</script>'
    return render_template('community/community_form.html', form=form)


@bp.route('/modify/<int:community_id>', methods=('GET', 'POST'))
@login_required
def modify(community_id):
    community = Community.query.get_or_404(community_id)
    if g.user != community.user:
        print("게시글 수정 권한 없음")
        print(g.user.email+"->"+community.user.email)
        return '<script>alert("수정권한이 없습니다.");location.href="/community/detail/' + str(community_id) + '"</script>'
    if request.method == 'POST':  # POST 요청
        form = CommunityForm()
        if form.validate_on_submit():
            if request.files['file']:
                filename = file_upload(request.files['file'])
                community.file = filename

            #로그
            print("게시글 수정됨")
            print(g.user.email+" -> "+community.user.email)
            print("제목 : "+community.subject+" -> "+form.subject.data)
            print("본문 : "+community.content+" -> "+form.content.data)
            ###

            community.subject = form.subject.data
            community.content = form.content.data
            community.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()

            return '<script>alert("수정되었습니다.");location.href="/community/detail/' + str(community_id) + '"</script>'
    else:  # GET 요청
        form = CommunityForm(obj=community)
    return render_template('community/community_form.html', form=form)


@bp.route('/delete/<int:community_id>')
@login_required
def delete(community_id):
    community = Community.query.get_or_404(community_id)
    if g.user != community.user and g.user.email != "biteup@biteup.com":

        print("게시글 삭제 권한 없음")
        print(g.user.email+" -> "+community.user.email)
        return '<script>alert("삭제 권한이 없습니다.");location.href="/community/detail/' + str(community_id) + '"</script>'

    #로깅
    print("게시글 삭제됨")
    print(g.user.email+" -> "+community.user.email)
    print("제목 : " + community.subject)
    print("본문 : " + community.content)
    ####

    db.session.delete(community)
    db.session.commit()
    return '<script>alert("삭제되었습니다.");location.href="/community/list"</script>'


@bp.route('/file_download/<string:file_name>')
@login_required
def file_download(file_name):
    try:
        path = os.getcwd()
        UPLOAD_FOLDER = os.path.join(path, 'pybo\\static\\upload_file\\')
        file_name = UPLOAD_FOLDER + file_name
        print(file_name)
        print("file_download success")
    except:
        print("file_download fail")
        return '<script>alert("error");</script>'
    return send_file(file_name, mimetype='image/png', as_attachment=True)


def file_upload(file):
    print("file_upload")
    filename = secure_filename(file.filename)
    file.save(UPLOAD_FOLDER + "\\" + filename)
    return filename
