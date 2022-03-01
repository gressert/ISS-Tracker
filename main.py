import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 42.166679
MY_LONG = -83.781319
MY_EMAIL = "testinggggggggggg1@gmail.com"
PASSWORD = "Hellome1"


def near_ISS():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5  and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = int(datetime.now().hour)

    if time_now >= sunset or time_now <= sunrise:
        return True


while near_ISS() and is_dark():
    time.sleep(60)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="testinggggggggggg2@gmail.com",
            msg=f"Subject:The ISS is overhead!\n\nLook up!"
        )
