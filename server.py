from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') 
app.config['MYSQL_DB'] = 'maindatabase'
 
mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        unique_id = str(uuid.uuid4())

        name = bcrypt.generate_password_hash(request.form['name']).decode('utf-8')
        email = bcrypt.generate_password_hash(request.form['email']).decode('utf-8')
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO py_user (id, name, email, password) VALUES (%s, %s, %s, %s)', (unique_id, name, email, password))
        mysql.connection.commit()
     
        cursor.close()

        return redirect('/registered')
    return render_template('index.html')

@app.route("/registered")
def registered():
    return render_template('registered.html')

