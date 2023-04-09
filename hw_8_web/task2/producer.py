import random

from faker import Faker
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


def main(n):
    fake = Faker()

    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        preferred_contact_method = random.choice(["email", "sms"])
        address = fake.address()
        contact = Contact(
            fullname=fullname,
            email=email,
            phone=phone,
            is_sent=False,
            preferred_contact_method=preferred_contact_method,
            address=address,
        )
        contact.save()

        message = str(contact.id)

        send_method = "sms" if contact.preferred_contact_method == "sms" else "email"

        channel.basic_publish(
            exchange="contact_exchange",
            routing_key=send_method,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    main(10)
