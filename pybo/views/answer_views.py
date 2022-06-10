from datetime import datetime
from .auth_views import login_required
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Community, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:community_id>', methods=('POST',))
@login_required
def create(community_id):
    form = AnswerForm()
    community = Community.query.get_or_404(community_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        community.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('community.detail', community_id=community_id))
    return render_template('community/community_detail.html', community=community, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    form = AnswerForm(obj=answer)
    # 보안
    # if g.user != answer.user:
    #     # flash('수정권한이 없습니다')
    #     print("수정 권한 없음")
    #     print(g.user+" "+answer.user)
    #     return '<script>alert("수정권한이 없습니다");location.href="/answer/detail/' + str(answer.community.id) + '"</script>'
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return '<script>alert("수정되었습니다.");location.href="/community/detail/' + str(answer.community.id) + '"</script>'

    return render_template('answer/answer_form.html', form=form)


@bp.route('/delete/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    community_id = answer.community.id
    if g.user != answer.user and g.user.email != "biteup@biteup.com":
        print("삭제 권한 없음")
        print(g.user.email+" -> "+answer.user.email)
        return '<script>alert("삭제권한이 없습니다");location.href="/community/detail/'+str(community_id)+'"</script>'
    else:
        db.session.delete(answer)
        db.session.commit()
        print("댓글이 삭제되었음")
        print(g.user.email+" -> "+answer.user.email)
    return '<script>alert("삭제되었습니다.");location.href="/community/detail/'+str(community_id) + '"</script>'
