from .melipayamak import Api
from risos.celery import app
import requests

username = '09129472900'
password = '6322'
api = Api(username, password)

# @app.task
# def send_sms(phone_number, msg):
#     # customer = Customer.objects.get(id=customer_id)
#     # if customer:
#     #     text = text.replace("!!first_name!!",customer.billing_first_name)
#     #     text = text.replace("!!last_name!!", customer.billing_last_name)
#     #     text = text.replace("!!address_1!!", customer.billing_address_1)
#     #     text = text.replace("!!city!!", customer.billing_city)
#     #     text = text.replace("!!state!!", customer.billing_state)
#     #     text = text.replace("!!phone!!", customer.billing_phone)
#     #     text = text.replace("!!postcode!!", customer.billing_postcode)
#     sms = api.sms()
#     to = phone_number
#     _from = '50004001472900'
#     # text = 'تست وب سرویس ملی پیامک'
#     msg = "کد تایید اپلیکیشن ریسوس" + " : " + msg
#     response = sms.send(to, _from, msg)
#     print(response)



@app.task
def send_sms(phone_number, msg):
    url = "https://console.melipayamak.com/api/send/shared/8f892b16c22a4b3f89072fb00ee45cb6"
    bodyId = 57270
    args = [str(phone_number), str(msg)]
    print(url)
    print(phone_number, "->", msg)

    body = { 
    "bodyId": bodyId, 
    "to": str(phone_number), 
    "args": args
    }
    r = requests.post(url, json=body)
    print(r.text)
    print(r.status_code)