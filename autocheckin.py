import requests
import sys
from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta
import pytz
from tzlocal import get_localzone
import time
from math import trunc
from flight_config import flight_info

class Southwest_IOS():

	def __init__(self,reservation_num, first_name, last_name):
		# Pulled from proxying the Southwest iOS App
		# self.headers = {'Host': 'mobile.southwest.com',
		# 			'Content-Type': 'application/vnd.swacorp.com.mobile.reservations-v1.0+json',
		# 				'X-API-Key': 'l7xxab4b3533b8d54bad9df230deb96a6f90', 'Accept': '*/*'}
		self.headers = {'Host': 'mobile.southwest.com',
					'Content-Type': 'application/vnd.swacorp.com.mobile.reservations-v1.0+json',
						'X-API-Key': 'l7xxc981db8c38c84a3ea0a0c677ec2fc021', 'Accept': '*/*'} # New Key 
		self.reservation_num = reservation_num
		self.first_name = first_name
		self.last_name = last_name
		self.url = "https://mobile.southwest.com/api/extensions/v1/mobile/reservations/record-locator/{}?first-name={}&last-name={}".format(self.reservation_num, self.first_name, self.last_name)
		self.r = requests.get(url=self.url, headers=self.headers)
		self.body = self.r.json()
		

	def flight_checktime(self):
		if 'httpStatusCode' in self.body and self.body['httpStatusCode'] == 'NOT_FOUND':
			print(self.body['message'])
		else:
			for leg in self.body['itinerary']['originationDestinations']:
				departure_time = leg['segments'][0]['departureDateTime']
				airport = leg['segments'][0]['originationAirportCode']
				date = parse(departure_time)
				date_to_checkin = date - timedelta(days=1)
				return date_to_checkin 
				

	def checkin_attempt(self):
		passengers = []
		for passenger in self.body['passengers']:
			passengers.append({'firstName': passenger['secureFlightName']['firstName'], 'lastName': passenger['secureFlightName']['lastName']})

		self.headers['Content-Type'] = 'application/vnd.swacorp.com.mobile.boarding-passes-v1.0+json'
		url = "https://mobile.southwest.com/api/extensions/v1/mobile/reservations/record-locator/{}/boarding-passes".format(self.reservation_num)
		r = requests.post(url, headers=self.headers, json={'names': passengers})
		body = r.json()
		if 'httpStatusCode' in body and body['httpStatusCode'] == 'FORBIDDEN':
			print(body['message'])
			time.sleep(10)
		elif "passengerCheckInDocuments" in body:
			for checkinDocument in body['passengerCheckInDocuments']:
				for doc in checkinDocument['checkinDocuments']:
					print ("You got {}{}!".format(doc['boardingGroup'], doc['boardingGroupNumber']))
					exit()

def main():
	s = Southwest_IOS(reservation_num=flight_info['reservation'],first_name=flight_info['first_name'],last_name=flight_info['last_name'])
	time_to_checkin = s.flight_checktime()
	while True:
		date_now = datetime.now(pytz.utc).astimezone(get_localzone())
		if date_now >= time_to_checkin:
			print "The Time is: {}\nAttempting to Check-In Now\n".format(date_now)
			s.checkin_attempt()
		else:
			print "Check-In Time: {}\nCurrent Time: {}\nTime Left Until Check-In: {}\n".format(time_to_checkin,date_now,time_to_checkin - date_now)
			time.sleep(10)

			
main()
