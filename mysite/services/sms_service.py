import json

from twilio.rest import Client


class SMS:

    @classmethod
    def send_sms(cls, customer_phone, country_code, data):
        # Twilio Account SID and Auth Token
        account_sid = 'AC3c462b0fe4ec965b83a3bfc32002c18c'
        auth_token = 'fa682a42301591d1d54cde1537c513ef'
        client = Client(account_sid, auth_token)
        message = {
            'message': 'Your response is stored successfully',
            'data': data
        }
        body = json.dumps(message)
        client.messages.create(
            to=country_code + customer_phone,
            from_='+12568263201',
            body=body
        )
