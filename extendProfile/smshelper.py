from ippanel import Client

api_key = "TkHglMm5LV49fr_SaxnT2vzr2eW7KFHT3VNXBxrIwAY="
sms = Client(api_key)
pattern_code = "3op4py8h7b"
phone_number = "+985000125475"


def otp_send(recipient, otp):
    pattern_values = {
        "otp": otp,
    }
    bulk_id = sms.send(
        phone_number,  # originator
        [recipient],  # recipients
        "کد تایید شما در وبسایت ریسوس: "+otp,
    )
    # bulk_id = sms.send_pattern(
    #     pattern_code,  # pattern code
    #     phone_number,  # originator
    #     recipient,  # recipient
    #     pattern_values,  # pattern Fvalues
    # )
