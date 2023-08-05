import os
import random

from flask import (flash,
                   redirect,
                   request,
                   render_template,
                   url_for)
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_login import current_user

from config import Config
from app import app, db
from app.forms import PostForm
from app.models import Post


def getting_a_photo():
    """Получение случайного фото."""
    files = os.listdir(Config.PEOPLE_FOLDER)
    images = [file for file in files]
    images = random.choice(images)
    image_final = os.path.join(Config.PEOPLE_FOLDER, images)
    return image_final


@app.route('/')
def show_index():
    """Функция выводит случайный пост."""
    quantity = Post.query.count()
    if not quantity:
        return 'FEE'
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
            flash(f'Проверьте поля:"{title}" и "{text}"'
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
    pass
