from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    searchInput = StringField(
        "Поиск по названию, автору, isbn...",
    )
    submit = SubmitField("Submit")
