from flask import redirect, render_template, url_for, flash

from . import app
from .forms import URL_mapForm
from .models import URL_map, ShortIdGenerationError

NAME_NOT_FREE = 'Имя "{}" уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if not form.validate_on_submit():
        return render_template('url_map.html', form=form)
    if not form.custom_id.data:
        try:
            short_id = URL_map.get_unique_short_id()
        except ShortIdGenerationError as error:
            flash(str(error))
    else:
        short_id = form.custom_id.data
        if URL_map.get_url_map(short_id) is not None:
            flash(NAME_NOT_FREE.format(short_id),)
            return render_template('index.html', form=form)
    URL_map.create(form.original_link.data, short_id)
    return render_template(
        'url_map.html',
        form=form,
        url_map=url_for('short_view', short=short_id, _external=True))


@app.route('/<string:short>')
def short_view(short):
    return redirect(URL_map.get_url_map_or_404(short).original)
