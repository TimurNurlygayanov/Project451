from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Regexp


class LoginForm(Form):
    username = StringField('username', render_kw={"placeholder": "Username"},
                           validators=[InputRequired(), Regexp(r'^\S+$')])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                             validators=[InputRequired()])

    def validate(self):
        return Form.validate(self)


class RegisterForm(Form):
    username = StringField('username', render_kw={"placeholder": "Username"},
                           validators=[InputRequired(), Regexp(r'^\S+$')])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                             validators=[InputRequired()])

    def validate(self):
        return Form.validate(self)
