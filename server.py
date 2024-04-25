from flask import Flask, render_template, redirect, request
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import hashlib

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class PyUser(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        unique_id = str(uuid.uuid4())

        name = hashlib.sha256(request.form['name'].encode()).hexdigest()
        email = hashlib.sha256(request.form['email'].encode()).hexdigest()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        new_user = PyUser(id=unique_id, name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/registered')
    return render_template('index.html')

@app.route("/registered")
def registered():
    return render_template('registered.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
