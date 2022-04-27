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

logging.basicConfig(level=logging.DEBUG)

oauth_callback_url = "http://localhost:8885"
oauth_consumer_key = os.getenv("TWITTER_APP_CONSUMER_KEY")
oauth_consumer_secret = os.getenv("TWITTER_APP_CONSUMER_SECRET")
oauth_bearer_token = os.getenv("TWITTER_APP_BEARER_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")

nonce = secrets.token_urlsafe(32)

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

# print(parameters_to_sign_string)

parameters_to_sign_string = "POST&{}&".format(urllib.parse.quote(step_1_request_url,safe='')) + urllib.parse.quote(parameters_to_sign_string,safe='')

print(parameters_to_sign_string)

signing_key = "{}&{}".format(urllib.parse.quote(oauth_consumer_secret, safe=''), urllib.parse.quote(access_token_secret,safe='')).encode()
print(signing_key)

signature = hmac.new(signing_key, parameters_to_sign_string.encode(), hashlib.sha1)

request_signature = base64.encodebytes(signature.digest()).decode().rstrip("\n")


step_1_request_url_headers["oauth_signature"] = request_signature
print(step_1_request_url_headers)

step_1_response = requests.post(step_1_request_url,
                                params=step_1_request_url_parameters,
                                headers=step_1_request_url_headers)

print(step_1_response.text)
