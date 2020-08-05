from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField,FileField
from wtforms.validators import DataRequired, Email, Length

class PostForm(FlaskForm):
	title = StringField('Título', validators=[DataRequired(), Length(max=128)])
	title_slug = StringField('Título slug', validators=[Length(max=128)])
	content = TextAreaField('Contenido')
	submit = SubmitField('Enviar')
