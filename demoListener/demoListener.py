#!/usr/bin/env python
import pika
import os
import time
import json

host = os.environ.get('RABBITMQ_HOST', "localhost")
user = os.environ.get('RABBITMQ_DEFAULT_USER', "cisco")
passwd = os.environ.get('RABBITMQ_DEFAULT_PASS', "C1sco123")
queue = os.environ.get('RABBITMQ_QUEUE', "HackZurich16")

credentials = pika.PlainCredentials(user, passwd)
connection = None
while (None == connection):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
    except:
        connection = None
        print "Connection Failed, retry in 5 sec"
        time.sleep(5)
channel = connection.channel()

channel.queue_declare(queue=queue)

def callback(ch, method, properties, body):
    print(" [x] Received Message with length of %r" % len(body))
    jdata = json.loads(body)
    print json.dumps(jdata, indent=4, sort_keys=True)

channel.basic_consume(callback,queue=queue,no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()