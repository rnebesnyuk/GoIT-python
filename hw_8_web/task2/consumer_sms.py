import time
import pika

from models import Contact
import connect


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()


channel.exchange_declare(exchange="contact_exchange", exchange_type="direct")
channel.queue_declare(queue="email_queue", durable=True)
channel.queue_declare(queue="sms_queue", durable=True)
channel.queue_bind(
    exchange="contact_exchange", queue="email_queue", routing_key="email"
)
channel.queue_bind(exchange="contact_exchange", queue="sms_queue", routing_key="sms")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)
    if contact:
        print(f'Sending SMS...')
        time.sleep(0.5)
        contact.is_sent = True
        contact.save()
        print(f'SMS sent for contact {contact_id}, tag: {method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print(f'Contact {contact_id} not found')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sms_queue', on_message_callback=callback)
print(' [*] Waiting for SMS messages. To exit press CTRL+C')
channel.start_consuming()
