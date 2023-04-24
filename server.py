from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MYSQL_DB'] = 'bd_web_servers'
 
mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = bcrypt.generate_password_hash(request.form['name']).decode('utf-8')
        email = bcrypt.generate_password_hash(request.form['email']).decode('utf-8')
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO python (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        mysql.connection.commit()
     
        cursor.close()

        return redirect('/registered')
    return render_template('index.html')

@app.route("/registered")
def registered():
    return render_template('registered.html')

