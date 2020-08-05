from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField,FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class SignupForm(FlaskForm):
	name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Registrar')

class PostForm(FlaskForm):
	title = StringField('Título', validators=[DataRequired(), Length(max=128)])
	title_slug = StringField('Título slug', validators=[Length(max=128)])
	content = TextAreaField('Contenido')
	submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class DocumentForm(FlaskForm):
    upload = FileField('Documento', validators=[FileRequired(),FileAllowed(['pdf'])])
    submit = SubmitField('Subir')