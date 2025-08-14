from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    phone = StringField("Phone", validators=[
        DataRequired(),
        Regexp(r'^\+?\d{10,15}$', message="Invalid phone number")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address")
    submit = SubmitField("Submit")
