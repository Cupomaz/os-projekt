from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(message='Please select an image file'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 
                   message='Only image files are allowed (jpg, jpeg, png, gif, webp)')
    ])
    description = TextAreaField('Description', 
                               validators=[Optional(), Length(max=500, message='Description must be less than 500 characters')])
