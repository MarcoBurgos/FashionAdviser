from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Título del post', validators=[DataRequired()])
    subtitle = StringField('Sumario', validators=[DataRequired()])
    photo_url = StringField("Ingresa la URL de la foto", validators=[DataRequired()])
    section_type = SelectField(u'Elige una categoría para el post:',
                          choices=[('Fashion', 'Fashion'), ('Beauty', 'Beauty'),
                                   ('Fitness', 'Fitness'), ('Lifestyle','Lifestyle')])
    post_content = TextAreaField()
    submit = SubmitField('Submit')
