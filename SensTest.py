import RPi.GPIO as GPIO
import Adafruit_DHT
import time 
import datetime
import sqlite3

from flask(__name__)


from flask_sqlalchemy import create_engine, Column, Float, Integer,String
from flask_sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
dht_sensor = Adafruit_DHT.DHT11
dht_pin = 14

y1_channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(y1_channel, GPIO.IN)

engine = create_engine('sqlite:///piplant2.db', echo = True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    name = Column(String)
    pin = Column(Integer)



class Reading(Base):
    __tablename__ = 'reading'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    desc = Column(String)
    value = Column(Float)

Base.metadata.create_all(engine)

session = Session()
today = str(datetime.date.today())
dht_sensor1 = Sensor(date=today, name ="DHT11 Temp & RH", pin=14)
session.add([dht_sensor1])
session.commit()
session.close()

# conn = sqlite3.connect('piplant.db')
# c = conn.cursor()

# c.execute('''CREATE TABLE sensor
#              (add_date text, sensor_text text, sensor_pin integer)''')
# c.execute('''CREATE TABLE reading
#              (add_date text, sensor_text text, value real)''')

#add_date = str(datetime.date.today())
#c.execute('''INSERT INTO sensor VALUES (?,?,?)''',
 #            (add_date, 'DHT11 Temp & RH', dht_pin))                             
#c.execute('''INSERT INTO sensor VALUES (?,?,?)''',
 #            (add_date, 'Capacitive Moisture Sensor V 1.2', y1_channel))                             

while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    moisture_reading = GPIO.input(y1_channel)
    if moisture_reading == GPIO.LOW:
        moisture = "Sufficient Moisture."
        moisture_db = 1
    else:
        moisture = "Low moisture, irrigation needed"
        moisture_db = 0

    session = Session()
    temp_reading = Reading(date=today, desc = "Temperature", value=temperature) 
    hum_reading = Reading(date=today, desc = "Humidiy", value=humidity)   
    moisture_reading = Reading(date=today, desc = "Moisture", value=moisture_db)
    session.add_all([temp_reading,hum_reading]) 
    session.commit()   
    session.close()  

    print("Sensor data: Humidity = {0:0.2f} % Temp = {1:0.2f} deg C moisture: {2}".format(humidity, temperature, moisture))
    

     # c.execute('''INSERT INTO reading VALUES (?,?,?)''',
      #         (add_date, 'Temperature', temperature))
     # c.execute('''INSERT INTO reading VALUES (?,?,?)''',
      #         (add_date, 'Humidity', humidity))
     # c.execute('''INSERT INTO reading VALUES (?,?,?)''',
      #         (add_date, 'Soil Moisture 1 means good 0 means dry', moisture_db))   
    #  conn.commit()
                   
    time.sleep(10)
    
    