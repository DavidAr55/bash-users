from ssl import SSLContext
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import logging
import subprocess
import re
import os
from ansi2html import Ansi2HTMLConverter

app = Flask(__name__)

# Configuración del logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySql Connection
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'flask'
app.config['MYSQL_PASSWORD'] = 'flaskServer2024'
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
    # Verificar si el usuario ha iniciado sesión antes de intentar cerrar la sesión
    if 'user_name' in session:
        logging.info('Cierre de sesión de: %s', session['user_name'])
        flash('¡Has cerrado sesión correctamente!', 'success')
    else:
        # Si el usuario no ha iniciado sesión, simplemente redirigirlo a la página de inicio de sesión
        flash('No has iniciado sesión', 'warning')

    # Limpiar la sesión, independientemente de si el usuario ha iniciado sesión o no
    session.clear()

    # Redirigir al usuario a la página de inicio de sesión
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
    
    logging.info('El usuario con id "%s" fue eliminado de manera exitosa', id)
    flash('Usuario eliminado')
    return redirect(url_for('Index'))


@app.route('/terminal')
def terminal():
    try:
        # Ejecutar el comando 'neofetch' y capturar su salida
        result = subprocess.run(['neofetch'], capture_output=True, text=True)
        output = result.stdout
        
        # Eliminar los caracteres no deseados al principio y al final del output
        output_cleaned = re.sub(r'^\x1b\[.*?m|\x1b\[0m$', '', output, flags=re.M)
        
        # Convertir los códigos de escape ANSI a HTML
        conv = Ansi2HTMLConverter()
        output_html = conv.convert(output_cleaned)

        return render_template('terminal.html', output=output_html)
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la ejecución del comando
        app.logger.error("Error al ejecutar el comando 'neofetch': %s", str(e))
        # Devolver un mensaje de error genérico al usuario
        return "Ocurrió un error al ejecutar el comando 'neofetch'. Por favor, inténtalo de nuevo más tarde."


import subprocess
from flask import jsonify

@app.route('/execute/bash/command', methods=['POST'])
def execute_bash_command():
    # Obtener el comando enviado desde el formulario
    command = request.form.get('fname')

    try:
        # Ejecutar el comando y capturar su salida
        result = subprocess.run([command], shell=True, capture_output=True, text=True)

        # Verificar el código de retorno del proceso
        if result.returncode != 0:
            # Si el código de retorno no es 0, hubo un error
            error = result.stderr.strip()

            # Eliminar los caracteres no deseados al principio y al final del output
            error_cleaned = re.sub(r'^\x1b\[.*?m|\x1b\[0m$', '', error, flags=re.M)
            
            # Convertir los códigos de escape ANSI a HTML
            conv_error = Ansi2HTMLConverter()
            error_html = conv_error.convert(error_cleaned)

            return jsonify({'error': error_html})
        
        # Si el código de retorno es 0, el comando se ejecutó correctamente
        output = result.stdout

        # Eliminar los caracteres no deseados al principio y al final del output
        output_cleaned = re.sub(r'^\x1b\[.*?m|\x1b\[0m$', '', output, flags=re.M)

        # Convertir los códigos de escape ANSI a HTML
        conv = Ansi2HTMLConverter()
        output_html = conv.convert(output_cleaned)

        # Devolver la salida como una respuesta JSON
        return jsonify({'output': output_html})
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la ejecución del comando
        app.logger.error("Error al ejecutar el comando en la terminal: %s", str(e))
        # Devolver un mensaje de error como respuesta JSON
        return jsonify({'error': 'Ocurrió un error al ejecutar el comando en la terminal'})


@app.route('/logs')
def logs():
    try:
        with open('app.log', 'r') as f:
            log_content = f.readlines()
            log_content.reverse()
            log_content = '\n'.join(log_content)  # Unir las líneas en una sola cadena
        return render_template('logs.html', log_content=log_content)
    except Exception as e:
        # Registra la excepción en el registro del servidor
        app.logger.error("Error en la vista de logs: %s", str(e))
        # Devuelve un mensaje de error genérico al usuario
        return "Ocurrió un error al cargar los registros. Por favor, inténtalo de nuevo más tarde."



# Rutas a los archivos de certificado y clave privada
certfile = '/etc/letsencrypt/live/davidloera-flask.info/fullchain.pem'
keyfile = '/etc/letsencrypt/live/davidloera-flask.info/privkey.pem'

# Verificar si los archivos de certificado y clave privada existen
if os.path.exists(certfile) and os.path.exists(keyfile):
    # Crear un contexto SSL y cargar el certificado y la clave privada
    ssl_context = SSLContext()
    ssl_context.load_cert_chain(certfile, keyfile)
else:
    # Si los archivos no existen, imprimir un mensaje de error
    print("No se encontraron los archivos de certificado y clave privada")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=ssl_context)
