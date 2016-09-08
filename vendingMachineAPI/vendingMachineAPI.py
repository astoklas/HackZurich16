from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from Machine import Machine
import pika
import time
import os


app = Flask(__name__)

mycounter = 0
apsched = BackgroundScheduler()


@app.before_first_request
def initialize():
    apsched.add_job(background_loop, 'interval', seconds=delay)
    apsched.start()

@app.route("/")
def root():
    return m.retriveValue(), 200, {'Content-Type': 'application/json'}

@app.route("/help")
def help():
    print "Giving Help, similar to /stats"
    print m.statistics()
    return "Vending Machine Simulator API\nCounter %i\n%s" % (mycounter,m.statistics()), 200, {'Content-Type': 'application/json'}


@app.route("/refill")
def refill():
    m.refill()
    return "Refilled everything", 200, {'Content-Type': 'application/json'}

@app.route("/clean")
def clean():
    m.clean()
    return "Everything clean and shiny now", 200, {'Content-Type': 'application/json'}

@app.route("/stats")
def stats():
    result = m.statistics()
    return result, 200, {'Content-Type': 'application/json'}

@app.route("/reset")
def reset():
    m.reset()
    return "Reset machine", 200, {'Content-Type': 'application/json'}

@app.route("/security")
def security():
    return "Not impemented; All Security Events cleared", 200, {'Content-Type': 'application/json'}

@app.route("/suspend")
def suspend():
    apsched.pause()
    msg = "Suspended generation of events"
    return msg , 200, {'Content-Type': 'application/json'}


@app.route("/resume")
def resume():
    apsched.resume()
    return "Resumed generation of events", 200, {'Content-Type': 'application/json'}


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
    port = int(os.environ.get('PORT', '5000'))
    print "##################################"
    print "# Starting Machine Simulator     #"
    print "# (c) 2016 Cisco                 #"
    print "# Server: %s #" % (host.ljust(22))
    print "# Queue: %s #" % (queue.ljust(23))
    print "# User: %s #" % (user.ljust(24))
    print "# Password: %s #" % (passwd.ljust(20))
    print "# Delay: %s #" % (os.environ.get('DELAY', '2').ljust(23))
    print "# Port: %s #" % (os.environ.get('DELAY', '2').ljust(24))
    print "##################################"
    time.sleep(2)
    connection, channel = connect(host, user, passwd, queue, 10)
    m = Machine(5)

    app.run(host="0.0.0.0",port=port)