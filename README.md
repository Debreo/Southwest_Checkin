# Southwest_Checkin
A script that automates the Southwest Check-in process in attempt to increase chances of a better boarding position on the flight.


# Configuration:
Add your flight information within the dictionary contained in flight_config.py


# How to use:
A few hours before your, flight invoke the script with:

python autocheckin.py

The script will check the time of your flight and compare it with the current time on your system.
Southwest check-ins are usually allowed exactly 24 hours from your flights departure. The script will
continously check and sleep every 10 seconds until it is time to check in. Once the script detects it is now
24 hours prior to your flights departure it will attempt to invoke the API call to check 
you in. If the script is successful it will return your boarding group and boarding group number.
Otherwise it will go to sleep for 10 seconds and attempt to check in again.


#Issues

Some versions of openssl do not account for TLS. If you receive this error:

requests.exceptions.SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version

you may require pyopenssl to run the script.

pip install pyopenssl