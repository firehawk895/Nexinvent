import requests


def send_sms(mobile_no, message):
    url = 'https://api.msg91.com/api/sendhttp.php'
    params = {'mobiles': mobile_no,
              'authkey': "282401ANhbbb165d10814a", 'route': 4,
              'sender': "TESTIN",
              'message': message,
              'country': "91"}
    r = requests.get(url, params=params)
    # log errors here