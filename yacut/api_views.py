from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URL_map

ID_NOT_FOUND = 'Указанный id не найден'
MISSING_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
URL_ERROR = 'Указан недопустимый URL'
ERROR_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
NAME_NOT_FREE = 'Имя "{}" уже занято.'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URL_map.get_url_map(short_id)
    if not url:
        raise InvalidAPIUsage(ID_NOT_FOUND, 404)
    return jsonify({'url': url.original})


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    try:
        url = URL_map.create(data['url'], data.get('custom_id'), validate=True)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url.to_dict()), 201
