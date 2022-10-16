from datetime import datetime
from re import fullmatch
from flask import url_for
from random import choices

import validators

from . import db
from settings import (ORIGINAL_LEN,
                      SHORT_LEN,
                      CHARACTERS_SET,
                      CUSTOM_ID_LEN,
                      ITERATIONS_COUNT,
                      PATTERN
                      )

ID_NOT_FOUND = 'Указанный id не найден'
MISSING_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
URL_ERROR = 'Указан недопустимый URL'
ERROR_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
NAME_NOT_FREE = 'Имя "{}" уже занято.'
PATTERN_SHORT_ID = PATTERN + f'{{1,{SHORT_LEN}}}'
SHORT_ID_GENERATION_ERROR = 'Короткая ссылка не может быть создана'
ERROR_LEN_ORIGINAL = 'Ошибка. Длинна исходной ссылки не может превышать {}'


class ShortIdGenerationError(Exception):
    pass


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LEN), nullable=False)
    short = db.Column(db.String(SHORT_LEN), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('short_view', short=self.short, _external=True))

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    @staticmethod
    def get_url_map_or_404(short_id):
        return URL_map.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def get_url_map(short_id):
        return URL_map.query.filter_by(short=short_id).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(ITERATIONS_COUNT):
            short_id = ''.join(choices(CHARACTERS_SET, k=CUSTOM_ID_LEN))
            if not URL_map.get_url_map(short_id):
                return short_id
        raise ShortIdGenerationError(SHORT_ID_GENERATION_ERROR)

    @staticmethod
    def create(original, short_id=None, validate=False):
        if validate:
            if len(original) > ORIGINAL_LEN:
                raise ValueError(ERROR_LEN_ORIGINAL.format(ORIGINAL_LEN))
            if not validators.url(original):
                # validators.url.url(original) дает ошибку
                raise ValueError(URL_ERROR)
            if short_id in [None, ""]:
                short_id = URL_map.get_unique_short_id()
            elif not fullmatch(PATTERN_SHORT_ID, short_id):
                #  если сделать раздельную проверку, то все равно
                #  сообщение об ошибке можно использовать только стандартное
                #  иначе не пройдет тестирование
                #  поэтому добавил контроль длины исходной ссылки (см. выше)
                raise ValueError(ERROR_SHORT_LINK)
            if URL_map.get_url_map(short_id):
                raise ValueError(NAME_NOT_FREE.format(short_id))
        url = URL_map(original=original, short=short_id)
        db.session.add(url)
        db.session.commit()
        return url
