from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class DocumentForm(FlaskForm):
    upload = FileField('Documento', validators=[FileRequired(),FileAllowed(['pdf'])])
    submit = SubmitField('Subir')