from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp, ValidationError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import choices


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'
db = SQLAlchemy(app)


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('short_view', short=self.short, _external=True))

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])


class URL_mapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message=('Ошибка в написании URL')), ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(r'^[A-Za-z0-9]+$',
                   message='Только латинские буквы (маленькие, большие) и цифры')]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URL_map.query.filter_by(short=field.data).first():
            raise ValidationError(f'{field.data} уже используется!')


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data or get_unique_short_id()
        url = URL_map(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        flash(url_for('short_view', short=short, _external=True))
    return render_template('url_map.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original)


def get_unique_short_id():
    while True:
        short_id = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=6))
        if not URL_map.query.filter_by(short=short_id).first():
            return short_id


if __name__ == '__main__':
    app.run()