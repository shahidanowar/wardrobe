from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class ItemUploadForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory')
    ], validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    occasion = SelectField('Occasion', choices=[
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('sport', 'Sport')
    ], validators=[DataRequired()])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Upload')

class OutfitForm(FlaskForm):
    name = StringField('Outfit Name', validators=[DataRequired()])
    occasion = SelectField('Occasion', choices=[
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('sport', 'Sport')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Outfit')
