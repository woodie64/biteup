from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, \
    SelectField, SelectMultipleField, FieldList, SubmitField, FileField  # AgreeField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, Regexp


class AgreeForm(FlaskForm):
    checkbox = SelectField('동의', validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email('올바른 이메일 주소를 입력하세요.')])
    username = StringField('사용자 이름',
                           validators=[DataRequired(), Length(min=3, max=10, message=('3자에서 10자 이하로 입력해주세요.'))])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    passwd_answer = StringField('비밀번호 힌트 답변', validators=[DataRequired('30자 이내로 작성해주세요'), Length(min=1, max=30)])


class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class PasswordResetForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email('올바른 이메일 주소를 입력하세요.')])
    username = StringField('사용자 이름', validators=[DataRequired()])
    passwd_answer = StringField('비밀번호 힌트 답변', validators=[DataRequired(), Length(0, 30, message=())])


class PasswordResetConfirmForm(FlaskForm):
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])


class ContactForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email('올바른 이메일 주소를 입력하세요.')])
    username = StringField('사용자 이름', validators=[DataRequired()])
    subject = StringField('제목', validators=[DataRequired()])
    message = TextAreaField('내용', validators=[DataRequired()])


# 게시판
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class CommunityForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class NoticeForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


# 프로필
class EditProfileForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired(), Length(min=3, max=10, message=('3자에서 10자 이하로 입력해주세요.'))])
    location = StringField('주소', validators=[Length(0, 64)])
    about_me = TextAreaField('자기소개')
    submit = SubmitField('저장')


class EditPasswordForm(FlaskForm):
    password = PasswordField('현재 비밀번호', validators=[DataRequired()])
    password1 = PasswordField('새 비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('새 비밀번호 확인', validators=[DataRequired()])


class EditProfileAdminForm(FlaskForm):
    username = StringField('이름', validators=[Length(0, 64)])
    location = StringField('주소', validators=[Length(0, 64)])
    about_me = TextAreaField('자기소개')
    submit = SubmitField('저장')