import os
import secrets
import base64
import time
import logging
import datetime
import urllib.parse
import hmac
import hashlib

import requests

oauth_callback_url = "http://localhost:8885"
oauth_consumer_key = os.getenv("TWITTER_APP_CONSUMER_KEY")

#nonce = base64.b64encode(secrets.token_bytes(32))
nonce = secrets.token_urlsafe(32)
print(nonce)
logging.basicConfig(level=logging.DEBUG)

print(oauth_consumer_key)
print(str(datetime.datetime.now().timestamp()))

step_1_request_url = f"https://api.twitter.com/oauth/request_token"
step_1_request_url_parameters = {"oauth_callback": oauth_callback_url}
step_1_request_url_headers = {"oauth_consumer_key": oauth_consumer_key,
                              "Authorization": "OAuth",
                              "oauth_signature_method": "HMAC-SHA1",
                              "oauth_nonce": nonce,
                              "oauth_version": "1.0",
                              "oauth_timestamp": str(int(datetime.datetime.now().timestamp()))
                              }

parameters_to_sign_dict = {**step_1_request_url_parameters, **step_1_request_url_headers}
parameters_to_sign_string = "&".join(map(lambda k: "{}={}".format(urllib.parse.quote(k,safe=''), urllib.parse.quote(parameters_to_sign_dict[k], safe='')), sorted(parameters_to_sign_dict.keys(), key=lambda x:x.lower())))

print(parameters_to_sign_string)

parameters_to_sign_string = "POST&{}&".format(urllib.parse.quote(step_1_request_url,safe='')) + urllib.parse.quote(parameters_to_sign_string,safe='')

print(parameters_to_sign_string)

signing_key = b"CONSUMER_SECRET&TOKEN_SECRET"

signature = hmac.new(signing_key, parameters_to_sign_string, hashlib.sha1)

request_signature = signature.digest().encode("base64").rstrip('\n')

print(request_signature)

"""
step_1_response = requests.post(f"https://api.twitter.com/oauth/request_token",
                                params={"oauth_callback": oauth_callback_url},
                                headers={"oauth_consumer_key": oauth_consumer_key,
                                         "Authorization": "OAuth",
                                         "oauth_signature_method": "HMAC-SHA1",
                                         "oauth_nonce": nonce,
                                         "oauth_version": "1.0",
                                         "oauth_timestamp": str(int(datetime.datetime.now().timestamp()))
                                         })

print(step_1_response.text)
"""