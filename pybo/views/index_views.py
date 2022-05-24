from flask import Blueprint, render_template, request, url_for, g, flash, send_file
from werkzeug.utils import secure_filename
from pybo.views.auth_views import login_required

from .. import db
from ..forms import CommunityForm, AnswerForm
from ..models import Community, Answer, User

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
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
    community_list = community_list.paginate(page, per_page=5)
    return render_template('index/trade.html', community_list=community_list, page=page, kw=kw)


@bp.route('/exchange')
@login_required
def exchange():
    return render_template('index/exchange.html')


@bp.route('/testpage')
def testpage():
    return render_template('index/testpage.html')