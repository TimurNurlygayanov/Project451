from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Regexp


class LoginForm(FlaskForm):
    username = StringField('username', render_kw={"placeholder": "Username"},
                           validators=[InputRequired(), Regexp(r'^\S+$')])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                             validators=[InputRequired()])

    def validate(self):
        return FlaskForm.validate(self)


class RegisterForm(FlaskForm):
    username = StringField('username', render_kw={"placeholder": "Username"},
                           validators=[InputRequired(), Regexp(r'^\S+$')])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                             validators=[InputRequired()])

    def validate(self):
        return FlaskForm.validate(self)


class UploadSampleForm(FlaskForm):
    archived_images = FileField('archived_images', render_kw={"placeholder": "Archived images"},
                                validators=[
                                    FileRequired(message='File is required!'),
                                    FileAllowed(['zip'], message='Zip archives only!')
                                ])

    def validate(self):
        return FlaskForm.validate(self)


class UploadToRecognizeForm(FlaskForm):
    image = FileField('image', render_kw={"placeholder": "Image file"},
                      validators=[
                          FileRequired(message='Image is required!'),
                          FileAllowed(['png'], message='PNG files only!')
                      ])

    def validate(self):
        return FlaskForm.validate(self)
