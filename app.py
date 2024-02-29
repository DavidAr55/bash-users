from flask import Flask, render_template, request, redirect, url_for, flash, session
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
def login(): 
    return render_template('login.html')

@app.route('/verify_login', methods=['POST'])
def verify_login():
    if request.method == 'POST':
        user_name     = request.form['user_name']
        user_password = request.form['user_password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE user_name = %s AND user_password = %s', (user_name, user_password))
        my_user = cur.fetchone()
        cur.close()
        
        if my_user:
            session['user_name']       = my_user[1]
            session['user_permission'] = my_user[3]
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('Index'))
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('¡Has cerrado sesión correctamente!', 'success')
    return redirect(url_for('index'))


@app.route('/home')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()
    
    return render_template('index.html', users=data)


@app.route('/add_user', methods=['POST'])
def add_user():
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
        cur.close()

        flash('Usuario agregado correctamente')
        return redirect(url_for('Index'))
    

@app.route('/edit/<id>')
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    
    return render_template('edit-user.html', user=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        user_name       = request.form['username']
        user_password   = request.form['password']
        user_permission = request.form['level']
        
        # Obtenemos la fecha y hora actual
        now = datetime.now()
        updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET user_name = %s, user_password = %s, user_permission = %s, updated_at = %s WHERE id = %s", (user_name, user_password, user_permission, updated_at, id))
        mysql.connection.commit()
        cur.close()
        
        flash('Usuario editado con exito')
        return redirect(url_for('Index'))
        

@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    
    flash('Usuario eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)