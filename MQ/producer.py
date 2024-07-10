import pika
import faker
from datetime import datetime

from models import Contact

from dotenv import load_dotenv
import os

load_dotenv()

MQ_USERNAME = os.getenv('MQ_USERNAME')
MQ_PASSWORD = os.getenv('MQ_PASSWORD')
MQ_HOST = os.getenv('MQ_HOST')
MQ_PORT = os.getenv('MQ_PORT')

EXCHANGE = 'Messenger_Service'
QUEUE_SMS = 'task_sms'
QUEUE_EMAIL = 'task_email'

credentials = pika.PlainCredentials(username=MQ_USERNAME, password=MQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=credentials, virtual_host=MQ_USERNAME))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
channel.queue_declare(queue=QUEUE_SMS, durable=True)
channel.queue_declare(queue=QUEUE_EMAIL, durable=True)
channel.queue_bind(exchange=EXCHANGE, queue='task_sms')
channel.queue_bind(exchange=EXCHANGE, queue='task_email')

fake_data = faker.Faker("uk_UA")

def create_task(num:int):
    for i in range(num):
        task = Contact(
            fullname=fake_data.name(),
            email=fake_data.email(),
            phone_number=fake_data.phone_number(),
            address=fake_data.address(),
            favor=fake_data.boolean(),
            created_at=datetime.now(),
            processed_at=None,
            consumer='None'
        ).save()

        if task.favor:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=QUEUE_SMS,
                body=str(task.id).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
        else:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=QUEUE_EMAIL,
                body=str(task.id).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
        print(" [x] Sent %r" % task.fullname)
    connection.close()


if __name__ == '__main__':
    create_task(20)
