from flask import Blueprint, render_template
bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/')
def trade():
    return render_template('index/trade.html')


@bp.route('/')
def _list():
    # 조회
    community_list = Community.query.order_by(Community.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.community_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        community_list = community_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.community_id == Community.id) \
            .filter(Community.subject.ilike(search) |  # 질문제목
                    Community.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    community_list = community_list.paginate(page, per_page=10)
    return render_template('index/trade.html')


@bp.route('/exchange')
def exchange():
    return render_template('index/exchange.html')
