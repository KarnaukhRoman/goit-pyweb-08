from datetime import datetime

import pika
from models import Contact
import time
import json

from dotenv import load_dotenv
import os

load_dotenv()
MQ_USERNAME = os.getenv('MQ_USERNAME')
MQ_PASSWORD = os.getenv('MQ_PASSWORD')
MQ_HOST = os.getenv('MQ_HOST')
MQ_PORT = os.getenv('MQ_PORT')

credentials = pika.PlainCredentials(username=MQ_USERNAME, password=MQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=credentials, virtual_host=MQ_USERNAME))
channel = connection.channel()

QUEUE_EMAIL = 'task_email'
channel.queue_declare(queue=QUEUE_EMAIL, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
consumer = 'Data Center 1'

def callback(ch, method, properties, body):
    pk = body.decode()
    task = Contact.objects(id=pk, message_sent=False).first()
    if task and not task.favor:
        print(f" [x] Received {task.id} {task.fullname}")
        print(f" [x] Done: {method.delivery_tag} message for {task.fullname} to {task.email} sended")
        task.update(set__message_sent=True, set__consumer=consumer, set__processed_at=datetime.now())#.save()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_EMAIL, on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
