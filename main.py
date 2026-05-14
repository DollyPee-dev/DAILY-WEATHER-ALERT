from smtplib import SMTP
import os
import requests
from twilio.rest import Client

OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/forecast"

# Environment Variables
api_key = os.environ.get("WEATHER_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

my_email = os.environ.get("EMAIL")
my_password = os.environ.get("EMAIL_PASSWORD")

parameter = {
    "lon": 3.879290,
    "lat": 7.348720,
    "cnt": 4,
    "APPID": api_key,
}
response = requests.get(OPEN_WEATHER_API, params=parameter)
response.raise_for_status()

weather_data = response.json()["list"]

going_to_rain = False

for each_day in weather_data:
    each_day_id = each_day["weather"][0]["id"]
    if int(each_day_id) < 600:
        going_to_rain = True

print(response.status_code)

if going_to_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Remember to bring your umbrella today, it is going to Rain ☂️☔",
        from_="+18143287702",
        to="+2349071627407"
    )

    print(message.status)

    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)

        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject: Rainny Day\n\nRemember to bring your umbrella today, it is going to Rain"
        )