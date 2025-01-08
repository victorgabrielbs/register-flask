from flask import Flask, render_template, redirect, request, flash
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
import os
import uuid

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class PyUser(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=255)
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = PyUser.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        unique_id = str(uuid.uuid4())
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = PyUser(id=unique_id, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect('/registered')
    return render_template('index.html', form=form)

@app.route('/registered')
def registered():
    return render_template('registered.html')

if __name__ == '__main__':
    app.run(debug=True)
