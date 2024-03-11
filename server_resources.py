import psutil
import datetime
import time
import mysql.connector
import pytz

# Stteings
tz = pytz.timezone('America/Mexico_City')

def obtener_informacion():
    now = datetime.datetime.now(tz)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_io = psutil.net_io_counters()
    network_traffic_in = network_io.bytes_recv
    network_traffic_out = network_io.bytes_sent

    return timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out

def eliminar_datos_antiguos(connection):
    try:
        cursor = connection.cursor()
        fifteen_days_ago = datetime.datetime.now(tz) - datetime.timedelta(days=15)
        fifteen_days_ago_str = fifteen_days_ago.strftime("%Y-%m-%d %H:%M:%S")
        query = "DELETE FROM server_resources WHERE timestamp < %s"
        cursor.execute(query, (fifteen_days_ago_str,))
        connection.commit()
        cursor.close()
    except mysql.connector.Error as error:
        print("Error al eliminar datos antiguos de la base de datos:", error)

def insertar_en_bd(connection, data):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO server_resources (timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos:", error)

def main():
    while True:
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="flask",
                password="flaskServer2024",
                database="bash_users"
            )

            timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out = obtener_informacion()
            print("Valores obtenidos:", timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out)  # Agregar esta línea para depuración
            data = (timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out)
            insertar_en_bd(connection, data)
            eliminar_datos_antiguos(connection)
            time.sleep(10)
        except Exception as e:
            print("Error:", e)
        finally:
            if connection.is_connected():
                connection.close()

if __name__ == "__main__":
    main()
