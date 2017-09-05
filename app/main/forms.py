from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Email

class SubscribeForm(Form):
    email = StringField('Adresse mail', validators=[Email()])
    submit = SubmitField("S'inscrire")
