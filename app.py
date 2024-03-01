from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_mysqldb import MySQL
from datetime import datetime
import logging

app = Flask(__name__)

# Configuración del logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySql Connection
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'bash_users'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def root(): 
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verify_login', methods=['POST'])
def verify_login():
    if request.method == 'POST':
        # Log de solicitud de inicio de sesión
        logging.info('Intento de inicio de sesión de usuario: %s', request.form['user_name'])
        
        user_name     = request.form['user_name']
        user_password = request.form['user_password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE user_name = %s AND user_password = %s', (user_name, user_password))
        my_user = cur.fetchone()
        cur.close()
        
        if my_user:
            session['user_name']       = my_user[1]
            session['user_permission'] = my_user[3]
            logging.info('Inicio de sesión del usuario "%s" completado de manera exitosa', request.form['user_name'])
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('Index'))
        else:
            logging.warning('Inicio de sesión fallido de: %s', request.form['user_name'])
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')
    
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    logging.info('Cierre de sesión de: %s', session['user_name'])
    flash('¡Has cerrado sesión correctamente!', 'success')
    return redirect(url_for('login'))


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

        logging.info('Nuevo usuario "%s" agregado exitosamente', user_name)
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
        
        logging.info('Usuario "%s" actualizado exitosamente', user_name)
        flash('Usuario editado con exito')
        return redirect(url_for('Index'))
        

@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    
    logging.info('El usuario con id "%s" fue eliminado de manera exitosa', user_name)
    flash('Usuario eliminado')
    return redirect(url_for('Index'))


@app.route('/terminal')
def terminal():
    return render_template('terminal.html')


@app.route('/execute/bash/command', methods=['POST'])
def execute_bash_command():
    return 1


@app.route('/logs')
def logs():
    with open('app.log', 'r') as f:
        log_content = f.readlines()
        log_content.reverse()
    return render_template('logs.html', log_content=log_content)


if __name__ == '__main__':
    logging.info('Servidor iniciado')
    app.run(port=5000, debug=True)