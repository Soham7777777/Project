from flask import Blueprint, redirect, render_template, url_for, flash, request
from .forms import RegistrationForm, LoginForm, ResetPasswordForm
from Application.models import User
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from Application import mail, CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES, db
from instance import IFlaskDefaultConfiguration
from datetime import timedelta
from celery import shared_task

bp = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    static_folder='static',
    template_folder='templates'
)

# @shared_task
def send_confirmation_link(to_address, link, template, subject):
    msg =  Message(
        subject=subject,
        recipients=[to_address]
    )
    msg.html = render_template(template, confirmation_link=link, expires_in=CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES)
    mail.send(msg)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data).one_or_none()

        if  user is not None and \
            user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('Account.dashboard'))

        flash("You don't have an account yet!", 'danger')
        return redirect(url_for('Auth.register'))
    
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter(User.email==form.email.data).one_or_none() is not None:
            flash(f'User with email {form.email.data} already have an account.', 'info')
            return redirect(url_for('Auth.login'))

        token = create_access_token(
            identity=form.email.data,
            expires_delta=timedelta(minutes=CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES),
            additional_claims=dict(name=form.name.data, password=form.password.data)
        )
        link = IFlaskDefaultConfiguration.PREFERRED_URL_SCHEME + '://' + request.host + url_for('Auth.confirm_email', jwt=token)
        # send_confirmation_link.delay(to_address=form.email.data, link=link, template='auth/emails/email_verification.html', subject="User Verification Via Confirmation Link")
        send_confirmation_link(to_address=form.email.data, link=link, template='auth/emails/email_verification.html', subject="User Verification Via Confirmation Link")


        flash('Please verify your email address to continue', 'info')
        return render_template('blank.html')
        
    return render_template('auth/register.html', form=form)


@bp.get('/confirm_email')
@jwt_required()
def confirm_email():
    email = get_jwt_identity()
    if (user:=User.query.filter(User.email==email).one_or_none()) is not None:
        flash('Email has already been verified', 'info')
        return redirect(url_for('Auth.login'))

    claims = get_jwt()
    user = User(email=email, name=claims['name'], password=claims['password'])
    db.session.add(user)
    db.session.commit()

    flash('Email has been successfully verified, please login to continue', 'success')
    return redirect(url_for('Auth.login'))


@bp.get('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('Auth.login'))


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter(User.email==email).one_or_none()
        if user is None:
            flash("You don't have an account yet", "info")
            return redirect(url_for('Auth.register'))
        
        new_password = form.new_password.data
        token = create_access_token(
            identity=email,
            expires_delta=timedelta(minutes=CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES), 
            additional_claims=dict(password=new_password)
        )
        link = IFlaskDefaultConfiguration.PREFERRED_URL_SCHEME + '://' + request.host + url_for('Auth.confirm_reset_password', jwt=token)
        # send_confirmation_link.delay(to_address=email, link=link, template='auth/emails/reset_password.html', subject="Password Reset Confirmation Via Email")
        send_confirmation_link(to_address=email, link=link, template='auth/emails/reset_password.html', subject="Password Reset Confirmation Via Email")


        flash("Please check your email, confirmation to reset password has been sent to your email", "info")
        return render_template('blank.html')

    return render_template('auth/reset_password.html', form=form)


@bp.get('/confirm_reset_password')
@jwt_required()
def confirm_reset_password():
    email = get_jwt_identity()
    user = User.query.filter(User.email==email).one_or_none()
    if user is None:
        flash("You don't have an account yet", "info")
        return redirect(url_for('Auth.register'))

    claims = get_jwt()
    user.password = claims['password']
    db.session.add(user) 
    db.session.commit()

    flash("The password for your account has been reset, login to continue", "info")
    return redirect(url_for('Auth.login'))


@bp.get('/delete_account')
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash("Your account has been deleted permanently!", 'warning')
    return redirect(url_for('Auth.login'))