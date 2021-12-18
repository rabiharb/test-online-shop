from flask_wtf import FlaskForm
from flask import url_for, render_template
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from lebshop.db_models import User


class SignupForm(FlaskForm):
    def validate_user_name(self, username):
        if " " in username.data:
            raise ValidationError("Space Charater not allowed in username.")
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError("Username already exists!")

    def validate_email(self, email_adress):
        user = User.query.filter_by(email=email_adress.data.lower()).first()
        if user:
            raise ValidationError(
                f"Email Adress already exists! LOGIN INSTEAD?")

    user_name = StringField(label="User Name: ", validators=[
        DataRequired(message="User Name field is required."), Length(min=2, max=50, message="User Name must be between 2 and 50 characters long.")])
    email = StringField(label="Email Adress: ", validators=[
        DataRequired(message="Email Address field is required."), Email(), Length(min=8, max=200, message="Email Adress must be less than 200 characters long.")])
    password = PasswordField(label="Password: ", validators=[
        DataRequired(message="Password field is required."), Length(min=8, max=1000, message="Password must be between 8 and 1000 characters long.")])
    confirm_password = PasswordField(
        label="Confirm Password: ", validators=[EqualTo("password", message="Passwords don't match")])
    submit = SubmitField(label="SIGN ME UP")


class SigninForm(FlaskForm):

    unique_identifier = StringField(label="Username or Email Adress", validators=[
                                    DataRequired("Please Provide a valid Username or Email adress.")])
    password = PasswordField(label="Password: ", validators=[
        DataRequired(message="Password field is required."), Length(min=8, max=1000, message="Password must be between at least 8 characters long.")])
    submit = SubmitField(label="LOG ME IN")
