import requests
from datetime import datetime, time
import smtplib


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To use this program for yourself information below needs to be updated to your personal info
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Checks to see if user position is within +5 or -5 degrees of the ISS position.
def distance_from_iss():
    if -5 <= (iss_latitude-MY_LAT) <= 5 and -5 <= (iss_longitude-MY_LONG) <= 5:
        return True
    else:
        return False


def convert_utc_to_pst(time):
    # Converts the hour from UTC time to PST time
    time = (time-7) % 24
    return time


def check_if_dark(sunrise, sunset, current_time):
    if sunrise <= current_time <= sunset:
        return False
    else:
        return True


# Program alerts user if the ISS is close to their current position, and the time is after dark.
MY_LAT = 33.75
MY_LONG = -118.15

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

print(data)

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

print(f"{iss_latitude}, {iss_longitude}")


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

print(data)

sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

sunrise_minutes = int(data["results"]["sunrise"].split("T")[1].split(":")[1])
sunset_minutes = int(data["results"]["sunset"].split("T")[1].split(":")[1])

sunrise_hour = convert_utc_to_pst(sunrise_hour)
sunset_hour = convert_utc_to_pst(sunset_hour)

sunrise = time(sunrise_hour, sunrise_minutes)
sunset = time(sunset_hour, sunset_minutes)

print(sunrise)
print(sunset)

current_time = datetime.now().time()

print(current_time)

iss_is_close = distance_from_iss()
is_dark = check_if_dark(sunrise=sunrise, sunset=sunset, current_time=current_time)

print(iss_is_close)
print(is_dark)

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

if iss_is_close and is_dark:
    my_email = "example@email.com"
    password = "thisisyourpassword"

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs="recipient@email.com",
                        msg="Subject:ISS Is Close!\n\nThe ISS is nearby! Step outside and see if you can find it!")
    connection.close()
