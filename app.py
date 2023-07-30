import os
import random
from datetime import datetime

from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename


PEOPLE_FOLDER = os.path.join('static', 'people_photo')
IMAGES = set('jpg jpe jpeg png gif svg bmp'.split())


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FAMES'

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(124), nullable=False)
    image = db.Column(db.String(128))
    text = db.Column(db.Text, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class PostForm(FlaskForm):
    title = StringField(
        'Введите название тату',
        validators=[DataRequired(message='Поле обязательное!'),
                    Length(1, 124)]
    )
    text = TextAreaField(
        'Всё что хочется рассказать',
        validators=[DataRequired(message='Поле обязательное!')]
    )
    image = FileField(
        'Фото',
        validators=[FileAllowed(
            IMAGES,
            'Только фото!'
        )]
    )
    submit = SubmitField('Отправить')


def getting_a_photo():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [file for file in files]
    images = random.choice(images)
    image_final = os.path.join(app.config['UPLOAD_FOLDER'], images)
    return image_final


@app.route('/')
def show_index():
    quantity = Posts.query.count()
    if not quantity:
        return 'Пока пусто'
    offset_value = random.randrange(quantity)
    post = Posts.query.offset(offset_value).first()
    return render_template('index.html', images=getting_a_photo(), post=post)


@app.route('/post/<int:id>')
def post_view(id: int): # noqa
    post = Posts.query.get(id)
    return render_template('index.html', post=post)


@app.route('/add', methods=['GET', 'POST'])
def add_posts():
    form = PostForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(str(image))
        image_file = request.files['image']
        image_file.save(
            os.path.join(
                PEOPLE_FOLDER,
                filename
            )
        )
        post = Posts(
            title=form.title.data,
            image=filename,
            text=form.text.data,
        )
        post.image = filename
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_view'))
    return render_template('add_post.html', form=form)


if __name__ == '__main__':
    app.run()
