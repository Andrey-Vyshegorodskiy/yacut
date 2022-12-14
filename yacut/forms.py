from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from settings import ORIGINAL_LEN, PATTERN, SHORT_LEN

from .models import URL_map

LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле.'
ERROR_LINK = 'Ошибка в написании URL'
CUSTOM_ID_MESSAGE = 'Ваш вариант короткой ссылки'
CUSTOM_ID_ERROR = 'Только латинские буквы (маленькие, большие) и цифры'
SUBMIT_MESSAGE = 'Добавить'
VALIDATION_ERROR_MESSAGE = 'Имя {} уже занято!'
PATTERN_CUSTOM_ID = f'^{PATTERN}+$'


class URL_mapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=ORIGINAL_LEN),
            URL(require_tld=True, message=ERROR_LINK), ]
    )
    custom_id = StringField(
        CUSTOM_ID_MESSAGE,
        validators=[
            Length(max=SHORT_LEN),
            Optional(),
            Regexp(PATTERN_CUSTOM_ID, message=CUSTOM_ID_ERROR), ]
    )
    submit = SubmitField(SUBMIT_MESSAGE)

    def validate_custom_id(self, field):
        if field.data and URL_map.get_url_map(field.data):
            raise ValidationError(VALIDATION_ERROR_MESSAGE.format(field.data))
        return field.data