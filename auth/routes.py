import os
from urllib.parse import urlsplit

from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from app import db
from auth import bp
from auth.forms import LoginForm, RegistrationForm
from auth.models import User
from config import Config


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        if (User.query.filter_by(username=username).first() is not None
                and User.query.filter_by(email=email).first() is not None):
            flash(f'Проверьте поля:"{username}" и "{email}"'
                  f' - они могут быть не уникальными!')
            return render_template('register.html', form=form)
        avatar = form.avatar.data
        filename = secure_filename(str(avatar))
        file_avatar = request.files['avatar']
        file_avatar.save(
            os.path.join(
                Config.PEOPLE_FOLDER,
                filename
            )
        )
        user = User(
            username=form.username.data, # noqa
            email=form.email.data, # noqa
            avatar=filename # noqa
        )
        user.set_password(form.password.data)
        user.avatar = filename
        db.session.add(user)
        db.session.commit()
        flash('Успешная регистрация')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль!')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('show_index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('show_index'))
