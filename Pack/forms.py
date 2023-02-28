from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired , FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo , Email, ValidationError

from Pack import photos
from Pack.models import User
from flask_uploads import UploadSet, IMAGES, configure_uploads

class RegisterUser(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])
    # profile_picture = FileField(validators=[FileAllowed(photos, 'Only Images are allowed'),
    #                                         FileRequired(' File Field should not be Empty')])
    submit = SubmitField('Register')
    update = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User already Exist")


    def validate_email(self, email):
        useremail = User.query.filter_by(email=email.data).first()
        if useremail:
            raise ValidationError("E-mail already Exist")


class LoginUser(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Log in')



class AddPost(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    # user_id = SelectField('User ID',validators=[DataRequired()])
    submit = SubmitField('Add Post')
    update = SubmitField('Update Post')
