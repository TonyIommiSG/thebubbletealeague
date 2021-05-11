#security.forms.py
from flask import flash
from flask_security import RegisterForm,LoginForm
from btlstattracker.models import User
from wtforms import StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired

# class CustomLoginForm(LoginForm):
#     def check_password(self,password):
#         return check_password_hash(self.password,password)

class ExtendedRegisterForm(RegisterForm):

    username = StringField('Username', validators=[DataRequired()])

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
        # response = super(CustomLoginForm,self).valdiate()
        #
        # return response
