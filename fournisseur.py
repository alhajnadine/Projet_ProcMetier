import pika
import requests
import mysql.connector
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

# Initialize the database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "toor",
    "database": "bd_projet"
}
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Establish connection with RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue for receiving orders
channel.queue_declare(queue='order_queue')



def send_order(name, service):
    payload = {
        'name': name,
        'service': service
    }
    response = requests.post('http://localhost:8000/order', json=payload)
    return response.text

def process_order(name, service):
    # Confirm the order
    confirmation = input(f"Do you want to confirm the order from {name} for {service}? (yes/no): ")
    if confirmation.lower() == 'yes':
        # Insert the confirmed order into the database with current date and status as "order processing"
        insert_query = "INSERT INTO donnee (client, service, status, Date) VALUES (%s, %s, %s, %s)"
        print("Client added to the database")
        order_data = (name, service, 'order processing', datetime.now())
        db_cursor.execute(insert_query, order_data)
        db_connection.commit()

        # Retrieve the price of the confirmed order from the database
        price_query = "SELECT price FROM services WHERE service_name = %s"
        db_cursor.execute(price_query, (service,))
        price = db_cursor.fetchone()[0]

        # Return the price along with the order confirmation message
        return price, "Order received and confirmed."
    else:
        return None, "Order received but rejected."

@app.post("/order")
async def process_order_api(payload: dict):
    name = payload['name']
    service = payload['service']
    price, message = process_order(name, service)
    if price is not None:
        return {"message": message, "price": price}
    else:
        return {"message": message}

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
