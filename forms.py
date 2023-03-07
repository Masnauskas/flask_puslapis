from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed



class ContactForm(FlaskForm):
    name = StringField('Name:', [DataRequired()])
    email = StringField('Email:', [Email(message=('Email entered wrong.')), DataRequired()])
    body = TextAreaField('Your text here:', [DataRequired(), 
                                        Length(min=10, 
                                        message=('Message too short.'))])
    image = FileField('Upload your picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')
    
