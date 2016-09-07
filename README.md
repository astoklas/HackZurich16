# HackZurich16

This is a simple simulator of a vending machine which has a set of goods (100 units to 0) with a small api to interact with the machine.
Data is pushed to a rabbitmq

## Get started
Quick way: 
docker-compose build
docker-cmopose up

Machine exposes api on port 5000
Rabbitmq exposes queue on port 5672

see HackZurich16-Listener porject for an example of consuming events and processing.
