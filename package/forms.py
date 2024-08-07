from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Incorrect password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class IncomeForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(message='Amount required!'), NumberRange(min=1, message="Amount must be a positive number.")])
    source = StringField('Source', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Income')

class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0, message="Amount must be a positive number.")])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Expense')

class SavingsGoalForm(FlaskForm):
    goal_amount = DecimalField('Goal Amount', validators=[DataRequired(), NumberRange(min=0, message="Amount must be a positive number.")])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Savings Goal')

class ContributionForm(FlaskForm):
    amount = DecimalField('Amount', places=2, validators=[DataRequired()])
    submit = SubmitField('Add Contribution')