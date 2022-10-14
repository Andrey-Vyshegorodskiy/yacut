from flask import redirect, render_template, url_for

from . import app
from .forms import URL_mapForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if not form.validate_on_submit():
        return render_template('url_map.html', form=form)
    original = form.original_link.data
    short_id = form.custom_id.data or URL_map.get_unique_short_id()
    URL_map.create(original, short_id)
    return render_template(
        'url_map.html',
        form=form,
        url_map=url_for('short_view', short=short_id, _external=True))


@app.route('/<string:short>')
def short_view(short):
    return redirect(URL_map.get_url_map_or_404(short).original)
