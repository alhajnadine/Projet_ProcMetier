import requests
import mysql.connector
from fastapi import FastAPI
import pika

app = FastAPI()

# Configuration de la base de données
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "toor",
    "database": "bd_projet"
}

# Fonction pour initialiser la connexion à la base de données
def initialize_database():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("Database connection successful.")
        return connection, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Fonction pour fermer la connexion à la base de données
def close_database(connection, cursor):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")
    except Exception as e:
        print(f"Error closing database connection: {e}")

# Fonction pour obtenir le nombre de commandes à passer
def get_number_of_orders():
    try:
        num_orders = int(input("How many orders do you want to place? "))
        return num_orders
    except ValueError:
        print("Please enter a valid number.")
        return get_number_of_orders()

# Fonction pour mettre à jour le statut du service dans la base de données
def update_status(cursor, service):
    try:
        update_query = "UPDATE donnee SET status = 'order done' WHERE service = %s"
        cursor.execute(update_query, (service,))
        db_connection.commit()
        print("Order Status updated")
    except Exception as e:
        print(f"Error updating order status: {e}")

# Fonction pour envoyer une commande au fournisseur
def send_order(name, service, cursor):
    try:
        payload = {
            'name': name,
            'service': service
        }
        response = requests.post('http://localhost:8000/order', json=payload).json()

        if 'price' in response:
            price = response['price']
            print(f"The price for {service} is {price}.")
            price_confirmation = input("Do you want to proceed with the order for this price? (yes/no): ")
            if price_confirmation.lower() == 'yes':
                # Envoi d'un message à RabbitMQ pour notifier le fournisseur
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='provider_queue', durable=True)
                channel.basic_publish(exchange='', routing_key='provider_queue', body=f"Client confirmed order: {name} - {service}")
                print("Notification sent to provider.")
                connection.close()

                # Mise à jour du statut à 'order done' dans la base de données
                update_status(cursor, service)

                return response
            else:
                return {"message": "Order canceled."}
        else:
            return response
    except Exception as e:
        print(f"Error sending order: {e}")

# Route pour traiter les commandes
@app.post("/order")
async def process_order(payload: dict):
    name = payload['name']
    service = payload['service']
    return send_order(name, service, db_cursor)

if __name__ == "__main__":
    try:
        # Initialisation de la connexion à la base de données
        db_connection, db_cursor = initialize_database()

        if db_connection and db_cursor:
            num_orders = get_number_of_orders()
            for i in range(num_orders):
                name = input(f"Enter name for order {i + 1}: ")
                service = input(f"Enter service for order {i + 1}: ")
                response = send_order(name, service, db_cursor)
                print(response)
    finally:
        # Fermeture de la connexion à la base de données
        close_database(db_connection, db_cursor)
