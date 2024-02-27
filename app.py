from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySql Connection
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'bash_users'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    
    return render_template('index.html', users=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        user_name       = request.form['username']
        user_password   = request.form['password']
        user_permission = request.form['level']
        
        # Obtenemos la fecha y hora actual
        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # print(f"user_name: {user_name}\nuser_password: {user_password}\nuser_permission: {user_permission}")
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (user_name, user_password, user_permission, created_at) VALUES (%s, %s, %s, %s)', (user_name, user_password, user_permission, created_at))
        mysql.connection.commit()

        flash('Usuario agregado correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()
    
    return render_template('edit-user.html', user=data[0])

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    
    flash('Usuario eliminado')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)