import Telstra_Messaging
from Telstra_Messaging.rest import ApiException
import requests
from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file

def generate_text(number, message):
    # create an instance of the API class
    api_instance = Telstra_Messaging.AuthenticationApi()
    client_id = "Agl2rsjQ0fbLC1xqPGDNve2Oianci7wK" # str |
    client_secret = "eWJoCzsYcTk2ITRl" # str |
    grant_type = 'client_credentials' # str |  (default to client_credentials)

    try:
        # Generate OAuth2 token
        api_response = api_instance.auth_token(client_id, client_secret, grant_type)
        access_token = api_response.__getattribute__('access_token')

        configuration = Telstra_Messaging.Configuration()
        configuration.access_token = access_token

        api_instance = Telstra_Messaging.MessagingApi(Telstra_Messaging.ApiClient(configuration))
        payload = {
                    "to": number,
                    "validity":"60",
                    "body": message
                    }

        try:
            # Send SMS
            api_response = api_instance.send_sms(payload)
        except ApiException as e:
            print("Exception when calling MessagingApi->send_sms: %s\n" % e)

    except ApiException as e:
        print("Exception when calling AuthenticationApi->auth_token: %s\n" % e)



    return "text sent"

class Text(Resource):
    def get(self):
        number = request.args['number']
        text = request.args['text']
        generate_text(number, text)
        return "text sent"

    


