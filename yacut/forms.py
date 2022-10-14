from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import (DataRequired, Length, Optional, URL, Regexp,
                                ValidationError)

from .models import URL_map
from settings import ORIGINAL_LEN, SHORT_LEN, PATTERN


LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле.'
ERROR_LINK = 'Ошибка в написании URL'
CUSTOM_ID_MESSAGE = 'Ваш вариант короткой ссылки'
CUSTOM_ID_ERROR = 'Только латинские буквы (маленькие, большие) и цифры'
SUBMIT_MESSAGE = 'Добавить'
VALIDATION_ERROR_MESSAGE = 'Имя {} уже занято!'


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
            Regexp(f'^{PATTERN}+$', message=CUSTOM_ID_ERROR), ]
    )
    submit = SubmitField(SUBMIT_MESSAGE)

    def validate_custom_id(self, field):
        if field.data and URL_map.query.filter_by(short=field.data).first():
            raise ValidationError(VALIDATION_ERROR_MESSAGE.format(field.data))
