from flask import flash, redirect, render_template, url_for
from random import choices

from . import app, db
from .forms import URL_mapForm
from .models import URL_map


def get_unique_short_id():
    kit = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    while True:
        short_id = ''.join(choices(kit, k=6))
        if not URL_map.query.filter_by(short=short_id).first():
            return short_id


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
