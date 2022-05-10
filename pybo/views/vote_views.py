from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Community, Notice, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/community/<int:community_id>/')
@login_required
def community(community_id):
    _community = Community.query.get_or_404(community_id)
    if g.user == _community.user:
        # flash('본인이 작성한 글은 추천할 수 없습니다')
        # return '<script>alert("본인이 작성한 글은 추천할 수 없습니다.");</script>'
        return '<script>alert("본인이 작성한 글은 추천할 수 없습니다.");location.href="/community/detail/' + str(community_id) + '"</script>'
    else:
        _community.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('community.detail', community_id=community_id))


@bp.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        # flash('본인이 작성한 글은 추천할 수 없습니다')
        #return '<script>alert("본인이 작성한 글은 추천할 수 없습니다.");</script>'
        return '<script>alert("본인이 작성한 글은 추천할 수 없습니다.");location.href="/community/detail/' + str(answer_id) + '"</script>'
    else:
        _answer.voter.append(g.user)
        db.session.commit()
        return '<script>alert("추천되었습니다.");location.href="/answer/' + str(answer_id) + '"</script>'
    return redirect(url_for('community.detail', community_id=_answer.community.id))


# Notice

# @bp.route('/notice/<int:notice_id>/')
# @login_required
# def notice(notice_id):
#     _notice = Notice.query.get_or_404(notice_id)
#     if g.user == _notice.user:
#         flash('본인이 작성한 글은 추천할 수 없습니다')
#     else:
#         _notice.voter.append(g.user)
#         db.session.commit()
#     return redirect(url_for('notice.detail', notice_id=notice_id))
#
#
# @bp.route('/answer/<int:answer_id>/')
# @login_required
# def answer(answer_id):
#     _answer = Answer.query.get_or_404(answer_id)
#     if g.user == _answer.user:
#         flash('본인이 작성한 글은 추천할 수 없습니다')
#     else:
#         _answer.voter.append(g.user)
#         db.session.commit()
#     return redirect(url_for('notice.detail', notice_id=_answer.notice.id))