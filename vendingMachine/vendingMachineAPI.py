from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from Machine import Machine
import pika
import time
import os


app = Flask(__name__)

mycounter = 0


@app.before_first_request
def initialize():
    apsched = BackgroundScheduler()
    apsched.add_job(background_loop, 'interval', seconds=delay)
    apsched.start()

@app.route("/")
def root():
    return "Vending Machine Simulator API\nCounter %i\n%s" % (mycounter,m.retriveValue())

@app.route("/refill")
def refill():
    return "Refilled everything"

@app.route("/clean")
def clean():
    return "Everything clean and shiny now"

@app.route("/security")
def security():
    return "All Security Events cleared"


if __name__ == "__main__":

    def background_loop():
        global mycounter
        mycounter = mycounter + 1
        channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=m.nextIteration())
        return

    def connect(myhost, myuser, mypasswd, myqueue='HackZurich16', maxRetries=6):
        myconnection = None
        errorCount = 1
        while (myconnection is None) and (errorCount < maxRetries):
            print "Connection attempt ", errorCount
            try:
                credentials = pika.PlainCredentials(myuser, mypasswd)
                myconnection = pika.BlockingConnection(pika.ConnectionParameters(host=myhost, credentials=credentials))
            except:
                myconnection = None
                errorCount += 1
                time.sleep(15)
        mychannel = myconnection.channel()
        mychannel.queue_declare(queue=myqueue)

        return myconnection, mychannel

    host = os.environ.get('RABBITMQ_HOST', "localhost")
    delay = int(os.environ.get('DELAY', '2'))
    user = os.environ.get('RABBITMQ_DEFAULT_USER', "cisco")
    passwd = os.environ.get('RABBITMQ_DEFAULT_PASS', "C1sco123")
    queue = os.environ.get('RABBITMQ_QUEUE', "HackZurich16")
    print "##################################"
    print "# Starting Machine Simulator     #"
    print "# (c) 2016 Cisco                 #"
    print "# Server: %s #" % (host.ljust(22))
    print "# Queue: %s #" % (queue.ljust(23))
    print "# User: %s #" % (user.ljust(24))
    print "# Password: %s #" % (passwd.ljust(20))
    print "# Delay: %s #" % (os.environ.get('DELAY', '2').ljust(23))
    print "##################################"
    time.sleep(2)
    connection, channel = connect(host, user, passwd, queue, 10)
    m = Machine(5)

    app.run()