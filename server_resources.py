import psutil
import datetime
import time
import mysql.connector
import pytz

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

def insertar_en_bd(data):
    try:
        connection = mysql.connector.connect(
            host     = "localhost",
            user     = "flask",
            password = "flaskServer2024",
            database = "bash_users"
        )

        cursor = connection.cursor()
        query = "INSERT INTO server_resources (timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos:", error)

def main():
    while True:
        timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out = obtener_informacion()
        print("Valores obtenidos:", timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out)  # Agregar esta línea para depuración
        data = (timestamp, cpu_usage, memory_usage, disk_usage, network_traffic_in, network_traffic_out)
        insertar_en_bd(data)
        time.sleep(10)

if __name__ == "__main__":
    main()
