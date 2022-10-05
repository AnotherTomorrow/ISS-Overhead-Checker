import smtplib
import requests
from datetime import datetime
import time

my_email = "YourEmailHere"
password = "YourPasswordHere"

MY_LAT = """Your Lat here in an int data type"""
MY_LONG = """Your Long here in an int data type"""


# check to see if the ISS is overhead and within viewing distance from your latitude/longitude.
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# Checks to see if it is nighttime, so we don't go outside and stare at the sun.
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour_now = time_now.hour

    if hour_now >= sunset or hour_now <= sunrise:
        return True


# While the program is running it checks every 60 seconds to see if the ISS is viewable overhead and sends an email.
while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="ReceivingEmailHere",
                                msg="Subject: The ISS is above you!\n\nLook up!")
