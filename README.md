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
simple statistics on the simulator
{
  "msgcount": 10,
  "start": "14/09/2016-08:35:30 UTC",
  "lastfill": "14/09/2016-08:35:30 UTC",
  "cleancount": 0,
  "fillcount": 0,
  "resetcount": 0,
  "lastclean": "14/09/2016-08:35:30 UTC",
  "lastreset": "14/09/2016-08:35:30 UTC",
  "id": "3ff93afb-6b90-4186-a404-8554209fbb8e"
}

http://machine:5000/reset
performs a machine reset (refill, clean)

http://machine:5000/suspend
stops event generation

http://machine:5000/resume
resumes event generation

## Json Object
// 20160914103609
// http://64.100.10.56:5000/

{
  "timestamp": "14/09/2016-08:35:30 UTC",
  "type": "vendingmachine",
  "id": "3ff93afb-6b90-4186-a404-8554209fbb8e",
  "data": [
    {
      "unit": "%",
      "type": "level",
      "id": 0,
      "value": 100,
      "description": "Supply Fill Level"
    },
    {
      "unit": "%",
      "type": "level",
      "id": 1,
      "value": 100,
      "description": "Supply Fill Level"
    },
    {
      "unit": "%",
      "type": "level",
      "id": 2,
      "value": 100,
      "description": "Supply Fill Level"
    },
    {
      "unit": "%",
      "type": "level",
      "id": 3,
      "value": 97,
      "description": "Supply Fill Level"
    },
    {
      "unit": "%",
      "type": "level",
      "id": 4,
      "value": 98,
      "description": "Supply Fill Level"
    },
    {
      "unit": "C",
      "type": "env_temperatur",
      "id": 0,
      "value": 41,
      "description": "Environment Temperatur"
    },
    {
      "unit": "C",
      "type": "op_temperatur",
      "id": 0,
      "value": 6,
      "description": "Operational Temperatur"
    },
    {
      "unit": "%",
      "type": "humidity",
      "id": 0,
      "value": 13,
      "description": "Environment Humidity"
    },
    {
      "unit": "W",
      "type": "power",
      "id": 0,
      "value": 445,
      "description": "Power Consumption"
    }
  ],
  "msgcounter": 1
}

