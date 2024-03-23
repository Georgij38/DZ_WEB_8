import pika
from bson import ObjectId

from models import Contact


# Функція для імітації надсилання електронної пошти
def send_email(contact_id):
    print(f"We are sending an email to the contact with the ID {contact_id}")

# Функція для обробки отриманого повідомлення
def callback(ch, method, properties, body):
    print("Received message:", body)  # Додано для виведення значення body

    contact_id = str(ObjectId(body.decode()))
  # Конвертація байтового об'єкта в рядок, а потім у ObjectId

    contact = Contact.objects(id=contact_id).first()

    if contact:
        send_email(contact_id)
        contact.email_sent = True
        contact.save()
        print(f"Notification of contact withID {contact_id} processed and marked as sent.")
    else:
        print(f"Contact with ID {contact_id} not found in database.")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='contacts_queue')

# Встановлення зв'язку між чергою та функцією обробки повідомлень
channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages from the queue RabbitMQ. Click to exit CTRL+C')
channel.start_consuming()
