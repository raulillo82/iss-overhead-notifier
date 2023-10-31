import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 42.8465088 # Your latitude
MY_LONG = -2.6724025 # Your longitude


#Your position is within +5 or -5 degrees of the ISS position.
def is_position_in_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    in_range = False
    if MY_LAT - iss_latitude <= abs(5) and MY_LONG - iss_longitude <= abs(5):
        in_range = True
        print("ISS over your head")
    return in_range


def is_night():

    is_night = False

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

    time_now = datetime.now()
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        is_night = True
        print("It is night!")
    return is_night

def send_email():
    PASSWORD_FILE = "./password"
    EMAIL_FILE = "./email"
    SMTP_SERVER = "smtp.gmail.com"

    try:
        with open(EMAIL_FILE) as email_file:
            email = email_file.readline()
        with open(PASSWORD_FILE) as password_file:
            password = password_file.readline()
    except FileNotFoundError:
        print(f"File {EMAIL_FILE} and/or {PASSWORD_FILE} not found! Terminating the program.")
    else:
        with smtplib.SMTP(SMTP_SERVER) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            msg = f"Subject:Look up the sky!\n\nThe ISS seems to be above you"
            " in the sky of Vitoria-Gasteiz!"
            connection.sendmail(from_addr=email, to_addrs=email, msg=msg)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    if is_position_in_range() and is_night():
        print("Sending email")
        send_email()
    print("Waiting for 60s before re-checking")
    time.sleep(60)

