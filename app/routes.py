import csv
import os
import random
from datetime import datetime

import click
from flask import (flash,
                   redirect,
                   request,
                   render_template,
                   url_for, abort)
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_login import current_user

from auth.models import User
from config import Config
from app import app, db
from app.forms import PostForm
from app.models import Post
from utils import getting_a_photo
from constants import ONE, TWELVE, INTERNAL_SERVER_ERROR


# Команда добавлена сюда а не в другую директорию.
@app.cli.command('load_test_data')
def load_test_data():
    """
    Создание тестовых данных.
    """
    db.create_all()
    with open('create_user.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(**row) # noqa
            db.session.add(user)
            db.session.commit()

    with open('data_for_start.csv', encoding='utf-8') as f:
        readers = csv.DictReader(f)
        for other_row in readers:
            # Для обхода ошибки вытягиваем из csv-файла значение timestamp
            # и делаем его форматом datetime.
            timestamp = datetime.strptime(
                other_row['timestamp'], # noqa
                '%Y-%m-%d%H:%M:%S.%f'
            )
            other_row['timestamp'] = timestamp # noqa
            post = Post(**other_row) # noqa
            db.session.add(post)
            db.session.commit()
    click.echo('Добавлены тестовые данные!')


@app.route('/')
def show_index():
    """Функция выводит случайный пост."""
    quantity = Post.query.count()
    if not quantity:
        abort(INTERNAL_SERVER_ERROR)
    offset_value = random.randrange(quantity)
    post = Post.query.offset(offset_value).first()
    return render_template(
        'index.html',
        images=getting_a_photo(),
        post=post
    )


@app.route('/post/<int:id>')
def post_view(id: int): # noqa
    """После создания поста, перенаправляет на этот пост."""
    post = Post.query.get_or_404(id)
    return render_template('index.html', post=post)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_posts():
    """Функция создания нового поста."""
    form = PostForm()
    if form.validate_on_submit():
        text = form.text.data
        title = form.title.data
        image = form.image.data
        if (Post.query.filter_by(text=text).first() is not None
                and Post.query.filter_by(title=title).first() is not None):
            flash(f'Проверьте поля с названием и описанием'
                  f' - они могут быть не уникальными!')
            return render_template('add_post.html', form=form)
        filename = secure_filename(str(image))
        image_file = request.files['image']
        image_file.save(
            os.path.join(
                Config.PEOPLE_FOLDER,
                filename
            )
        )
        post = Post(
            title=form.title.data,
            image=filename,
            text=form.text.data,
            user_id=current_user.id,
        )
        post.image = filename
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_view', id=post.id))
    return render_template('add_post.html', form=form)


@app.route('/all_posts', methods=['GET', 'POST'])
def all_posts():
    """Функция для вывода всех постов."""
    # Пагинация для постов
    page = request.args.get('page', ONE, type=int)
    posts = Post.query.paginate(page=page, per_page=TWELVE)
    return render_template('all_posts.html', posts=posts)


@app.route('/user_posts/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users_posts(user_id: int): # noqa
    """Переводит на страницу юзера."""
    page = request.args.get('page', ONE, type=int)
    selected_user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(
        user_id=user_id
    ).paginate(page=page, per_page=TWELVE)
    return render_template(
        'user_posts.html',
        posts=posts,
        selected_user=selected_user
    )
