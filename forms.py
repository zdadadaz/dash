from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField \
                    ,TextAreaField, SelectField, IntegerField,FloatField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class BlogForm(FlaskForm):
    username = SelectField('Username', choices=[], coerce=int)
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Addstock(FlaskForm):
    bprice = FloatField('bprice', validators=[DataRequired()])
    sprice = FloatField('sprice', validators=[DataRequired()])
    pprice = FloatField('pprice', validators=[DataRequired()])
    sell = FloatField('sell', validators=[DataRequired()])
    bdate = DateField('bdate', format='%Y-%m-%d')
    sid = FloatField('sid')
    ticker = FloatField('ticker')
    submit = SubmitField('Submit')

    