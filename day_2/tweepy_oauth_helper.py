import webbrowser
import os
import http.server
import logging
import sys
import functools

import tweepy

# 100_days_of_code_2022 day_2

# Set up basic logging for output
logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


TWITTER_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")

twitter_api_scopes = ["tweet.read",  "users.read", "offline.access"]

twitter_oauth_callback_url_ip = "127.0.0.1"
twitter_oauth_callback_url_proto = "http"
twitter_oath_callback_url_ports_to_try = [8888, 8880, 8080, 9977, 4356, 3307]


if twitter_oauth_callback_url_proto == "http" and int(os.environ.get("OAUTHLIB_INSECURE_TRANSPORT", 0)) != 1:
    logging.error("If using http as callback proto, the environment variable OAUTHLIB_INSECURE_TRANSPORT must be set to 1. See http://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html")
    sys.exit(-1)

oauth2_user_handler = None
http_server = None


class _AuthParametersCaptureRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Minimal handler for build in python3 httpd server. Captures the parameters made from callback URL to be
    used in continuing OAuth2 authentication flow
    """

    auth_response_dict = None

    # noinspection PyMissingConstructor
    def __init__(self, *args, auth_response_dict, **kwargs):
        self.auth_response_dict = auth_response_dict
        super(http.server.BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Authorization complete! You can return to app.")
        self.auth_response_dict["auth_response_path"] = self.path
        return self


# This is the one weird part of the process. The built in HTTP Server class does not have a way to pass information
# about a request it servers back to the main thread. The AuthParametersCaptureRequestHandler class is a hacky way
# to 'grab' the URL callback parameters when the Twitter OAuth2 flow passes control back to the script
auth_response_dict = dict()
AuthCaptureHandler = functools.partial(_AuthParametersCaptureRequestHandler, auth_response_dict=auth_response_dict)

for twitter_oath_callback_url_port in twitter_oath_callback_url_ports_to_try:

    # construct a full call back URL out of our parts
    twitter_oauth_callback_url = f"{twitter_oauth_callback_url_proto}://{twitter_oauth_callback_url_ip}:{twitter_oath_callback_url_port}/"

    logging.debug(f"Creating oauth2 helper with callback URL {twitter_oauth_callback_url}")
    # create a tweepy oauth handler with the current URL
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=TWITTER_CLIENT_ID,
        redirect_uri=twitter_oauth_callback_url,
        scope=twitter_api_scopes
    )

    # try to create a local http server listening at the callback URL
    try:
        http_server = http.server.HTTPServer((twitter_oauth_callback_url_ip, twitter_oath_callback_url_port),
                                             AuthCaptureHandler)
        logging.info(f"HTTP listener bound to {twitter_oauth_callback_url_ip} {twitter_oath_callback_url_port}")
    except Exception as e:
        logging.warning(f"Could not bind HTTP listener to {twitter_oauth_callback_url_ip} {twitter_oath_callback_url_port}. Going to try next port in list")
        logging.debug(f"bind exception is '{e}'")
        continue

    # HTTP listener was created, so we can break out of the loop trying the list of listening ports
    break

# If httpd is None the listener no subitle port was found, have to exit
if http_server is None:
    logging.error("Could not create httpd listener for callback capture. Exiting")
    sys.exit(-1)

# now that the tweepy oauth handler is ready and there is a local http server ready for the callback URL open the
# auth page at Twitter
logging.debug("OAuth auth URL is {}".format(oauth2_user_handler.get_authorization_url()))
webbrowser.open(oauth2_user_handler.get_authorization_url())

# Wait for the callback request
http_server.handle_request()

logging.debug(f"Auth response dict '{auth_response_dict}'")
# OAUTHLIB_INSECURE_TRANSPORT must be set to 1
access_credentials_dictionary = oauth2_user_handler.fetch_token(auth_response_dict["auth_response_path"])
logging.debug(f"Access credentials dictionary is {access_credentials_dictionary}")

client = tweepy.Client(bearer_token=access_credentials_dictionary["access_token"])

# This call would fail if client object wasn't authenticated
print(client.get_me(user_auth=False))
