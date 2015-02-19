#!/usr/bin/env python

import sqlite3
import time
from datetime import date , datetime
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


def logData(t, n):

	try:
		db = sqlite3.connect('/home/pi/Aqua/Aquaman/Aquaman/data.db')
		c = db.cursor()
		
		print n
		c.execute('insert into tempdata (temp, time) values (?, ?)', (t, n,))
		
		db.commit()
		print t
	except Exception as e:
		db.rollback()
		raise e
	finally:
		db.close()

def main():
	temp = sensor.get_temperature()
	n = datetime.now()
	# print temp
	logData(temp, n)

main()




