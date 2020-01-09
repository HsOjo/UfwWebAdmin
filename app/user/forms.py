from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    remember = BooleanField(label='记住登录状态')
    submit = SubmitField(label='登录')


class UserInfoEditForm(FlaskForm):
    password = PasswordField(label='密码', description='留空则不改变密码')
    submit = SubmitField(label='编辑')
