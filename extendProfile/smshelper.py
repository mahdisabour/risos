from .melipayamak import Api

username = 'gaatgallery'
password = '2488'
api = Api(username, password)


def send_sms(phone_number, msg):
    # customer = Customer.objects.get(id=customer_id)
    # if customer:
    #     text = text.replace("!!first_name!!",customer.billing_first_name)
    #     text = text.replace("!!last_name!!", customer.billing_last_name)
    #     text = text.replace("!!address_1!!", customer.billing_address_1)
    #     text = text.replace("!!city!!", customer.billing_city)
    #     text = text.replace("!!state!!", customer.billing_state)
    #     text = text.replace("!!phone!!", customer.billing_phone)
    #     text = text.replace("!!postcode!!", customer.billing_postcode)
    sms = api.sms()
    to = phone_number
    _from = '30008666971367'
    # text = 'تست وب سرویس ملی پیامک'
    msg = "کد تایید اپلیکیشن ریسوس" + " : " + msg
    response = sms.send(to, _from, msg)
    print(response)
