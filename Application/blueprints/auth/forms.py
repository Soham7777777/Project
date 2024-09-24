from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Application import MIN_NAME_SIZE, MAX_NAME_SIZE, MIN_PASSWORD_SIZE, MAX_PASSWORD_SIZE, NAME_CAN_CONTAIN, PASSWORD_CAN_CONTAIN


def nameValidator(form, field):
    value = field.data
    if  len(value) not in range(MIN_NAME_SIZE, MAX_NAME_SIZE + 1):
        raise ValidationError(f'name can have length between {MIN_NAME_SIZE} and {MAX_NAME_SIZE}')
    
    for char in value:
        if char not in NAME_CAN_CONTAIN:
            raise ValidationError(f'name can only contain upper or lower alphabets')

    
def passwordValidator(form, field):
    value = field.data
    if  len(value) not in range(MIN_PASSWORD_SIZE, MAX_PASSWORD_SIZE + 1):
        raise ValidationError(f'password can have length between {MIN_PASSWORD_SIZE} and {MAX_PASSWORD_SIZE}')

    for char in value:
        if char not in PASSWORD_CAN_CONTAIN:
            raise ValidationError(f'password can only contain upper/lower alphabets, numbers or punctuations')


class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=MIN_NAME_SIZE, max=MAX_NAME_SIZE), nameValidator], render_kw={"placeholder": "Username"}, default='', filters=[str.strip])
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"}, default='', filters=[str.strip])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_SIZE, max=MAX_PASSWORD_SIZE), passwordValidator], render_kw={"placeholder": "Password"}, default='', filters=[str.strip])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_SIZE, max=MAX_PASSWORD_SIZE), EqualTo('password', 'passwords are not matching'), passwordValidator], render_kw={"placeholder": "Retype Password"}, default='', filters=[str.strip])
    recaptcha = RecaptchaField()
    
    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"}, default='', filters=[str.strip])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_SIZE, max=MAX_PASSWORD_SIZE), passwordValidator], render_kw={"placeholder": "Password"}, default='', filters=[str.strip])
    remember_me = BooleanField("Remember Me", default=False)


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"}, default='', filters=[str.strip])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_SIZE, max=MAX_PASSWORD_SIZE), passwordValidator], render_kw={"placeholder": "Password"}, default='', filters=[str.strip])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_SIZE, max=MAX_PASSWORD_SIZE), EqualTo('new_password', 'passwords are not matching'), passwordValidator], render_kw={"placeholder": "Retype Password"}, default='', filters=[str.strip])
