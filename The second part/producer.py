import pika

from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue')


contacts = Contact.objects()
for contact in contacts:
    message = str(contact.id)
    channel.basic_publish(exchange='', routing_key='contacts_queue', body=message)

print("Contact message sent to RabbitMQ queue")


connection.close()
