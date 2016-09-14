# HackZurich16

This is a simple simulator of a vending machine which has a set of goods (100 units to 0) with a small api to interact with the machine.
Data is pushed to a rabbitmq

## Get started

###update Code: Change to the subdirectory HackZurich16 and perform git pull. Instruction to connect to the environment are provided speratly.

Quick way: 
docker-compose build
docker-cmopose up

Machine exposes api on port TCP/5000
Rabbitmq exposes queue on port TCP15001

see HackZurich16-Listener porject for an example of consuming events and processing.

## API
All requests are GET with no authentication or authorization.

http://machine:5000/
retrieves last data object from simulator

http://machine:5000/refill
Sets the Level Values again to 100 (for all levels at the same time)

http://machine:5000/clean
increases the clean counter and sets the date/time of the last clean to the current time

http://machine:5000/stats
simle statistics on the simulator

http://machine:5000/reset
performs a machine reset (refill, clean)

http://machine:5000/suspend
stops event generation

http://machine:5000/resume
resumes event generation
