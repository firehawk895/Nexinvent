from celery import Celery
from twilio.rest import Client
from django.conf import settings
app = Celery('mvp', broker='pyamqp://guest@localhost//')


@app.task
def send_whatsapp(mobile_no, message, status_callback=None):
    account_sid = settings.TWILIO['SID']
    auth_token = settings.TWILIO['AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    to = "whatsapp:" + mobile_no
    message = client.messages.create(
        from_='whatsapp:+18335800088',
        body=message,
        to=to,
        status_callback=status_callback
    )
    print(message.sid)
