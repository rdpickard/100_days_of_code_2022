import os
import http.server
import logging
import sys
import time
import webbrowser
import functools
import json
import arrow

import jsonschema
import authlib.integrations.requests_client
# noinspection PyPackageRequirements
import pytwitter  # pip 'package' is python-twitter, module is pytwitter -RDP
import requests

# The Client ID of the Twitter application MUST be set in the environment variable TWITTER_CLIENT_ID

# Twitter application MUST be configured with OAuth2 enabled, as a Native App and the following Callback URLs
#
# http://127.0.0.1:8888
# http://127.0.0.1:8880
# http://127.0.0.1:8080
# http://127.0.0.1:9977
# http://127.0.0.1:4356
# http://127.0.0.1:3307
#
# Callback URLs could be changed to be whatever you want but the code needs to be changed accordingly with the
# values in local_ports_to_try and the value of listen_ip parameter of OAuth2AuthenticationFlowHelper. If the
# Twitter Application configuration has does not have the Callback URL list that contains the configured ip and port
# of this script the user will get an "Something went wrong!" message when trying to authorize the app

if sys.version_info < (3, 7):
    # script uses functools.partial which is a pretty recent capability
    print("Python 3.7 or later required to run")
    sys.exit(-1)

LOCAL_HTTPD_SERVER_PORTS_TO_TRY = [8888, 8880, 8080, 9977, 4356, 3307]

TWITTER_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")

logging.basicConfig(level=logging.DEBUG)

# The scopes requested of the Twitter OAUTH2 API on behalf of the user that will bleach their account
# To refresh temporary access token "offline.access" MUST be one of the requested scopes
twitter_api_scopes = ["tweet.read", "tweet.write", "users.read", "tweet.read",
                      "users.read", "like.write", "like.read", "follows.read",
                      "block.read",
                      "list.read",
                      "follows.write", "offline.access"]


class WrappedPyTwitterAPIRateLimitExceededException(pytwitter.PyTwitterError):
    pass


class WrappedPyTwitterAPIUnauthorizedException(pytwitter.PyTwitterError):
    pass


class WrappedPyTwitterAPIOAuth2FlowException(pytwitter.PyTwitterError):
    pass


class WrappedPyTwitterAPI(pytwitter.Api):
    oauth2_flow_called_back_auth_url = None

    def __init__(self, *args, **kwargs):
        super(WrappedPyTwitterAPI, self).__init__(*args, **kwargs)

    class _AuthParametersCaptureRequestHandler(http.server.BaseHTTPRequestHandler):
        """
        Minimal handler for build in python3 httpd server. Captures the parameters made from callback URL to be
        used in continuing OAuth2 authentication flow
        """

        wrapped_api = None

        # noinspection PyMissingConstructor
        def __init__(self, *args, wrapped_api, **kwargs):
            self.wrapped_api = wrapped_api
            super(http.server.BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization complete! You can return to app.")
            self.wrapped_api.oauth2_flow_called_back_auth_url = self.path
            return self

    def OAuth2AuthenticationFlowHelper(self, local_ports_to_try, listen_ip="127.0.0.1"):

        # Start a minimal local HTTPD listener to get the authorization details.
        # When the Twitter OAUTH2.0 process redirects the local HTTPD listener will get the request. This way the user
        # doesn't have to copy and paste strings or anything like that
        httpd_bound_port = None
        httpd = None

        # The built in python httpd server does not have a way to pass back information gathered from the request it
        # served. And the built in python httpd server creates its own instance of a handler on demand so my subclass
        # of the handler can't be initialized the way I want.
        # Also there isn't a way for inner classes to access it's outer class.
        # To get around this, use the function tools module to create a partial instance of
        # AuthParametersCaptureRequestHandler with a reference to the WrappedPyTwitterAPI stuffed in. It's a dirty way
        # to pass the auth url back to the OAuth2 flow
        AuthCaptureHandler = functools.partial(self._AuthParametersCaptureRequestHandler, wrapped_api=self)

        # Start an HTTPD listening on the first available ephemeral port
        for httpd_bound_port in local_ports_to_try:
            # noinspection PyBroadException
            try:
                httpd = http.server.HTTPServer((listen_ip, httpd_bound_port), AuthCaptureHandler)
                break
            except Exception as e:
                raise WrappedPyTwitterAPIOAuth2FlowException(f"Could not start http listener on port "
                                                             f"'{httpd_bound_port}' reason '{e}'")

        if httpd is None:
            raise WrappedPyTwitterAPIOAuth2FlowException(f"Could not start http listener on any port "
                                                         f"'{local_ports_to_try}'")
        else:
            logging.debug(f"HTTPD listening on port {httpd_bound_port}")

        twitter_auth_callback_redirect_url = f"http://{listen_ip}:{httpd_bound_port}/"

        twitter_user_auth_url, code_verifier, _ = api.get_oauth2_authorize_url(
            redirect_uri=twitter_auth_callback_redirect_url)

        # Open the URL in the default browser of the environment
        webbrowser.open(twitter_user_auth_url)

        # This should wait forever until the user clicks "Authorize App" on the Twitter site
        httpd.handle_request()

        # The AuthParametersCaptureRequestHandler passed to the httpd server will set the class variable
        # oauth2_flow_called_back_auth_url to 'capture' the parameters Twitter provides to continue the oauth flow.

        # Using the 'state' and 'code' values in the redirect URL that the Twitter OAUTH 2 calls, request a bearer token
        # for the user context. The user context is what lets this script make changes on behalf of the user that
        # "Authorized App"
        auth_credentials = api.generate_oauth2_access_token(self.oauth2_flow_called_back_auth_url,
                                                            code_verifier,
                                                            redirect_uri=twitter_auth_callback_redirect_url)

        # This bearer token in these credentials will expire!
        #
        # Unlike the bearer token value on the Twitter application dashboard, this token will expire in 2 hours.
        # The Twitter documentation is kind of confusing. However pytwitter will work fine while the token is valid.
        # After it has expired refresh_token will need to be called.

        api.set_access_token(auth_credentials['access_token'])

        return auth_credentials

    def set_access_token(self, access_token):
        """
        Sets the API to use the provided access token for authenticated requests
        :param access_token: Token value from Twitter OAuth2
        :return: None
        """
        self._auth = authlib.integrations.requests_client.OAuth2Auth(
            token={"access_token": access_token, "token_type": "Bearer"}
        )

    def refresh_access_token(self, refresh_token):
        """
        Use the refresh_token value to get a new temporary access token. On success the API object will be updated
        to use the new token. set_access_token does not need to be called directly.

        To refresh temporary access token "offline.access" MUST be one of the requested scopes

        :param refresh_token: The token provided by the last successful authentication or refresh
        :return: The new auth deatils, including the next refresh token
        :raises PyTwitterError: If refresh request did not return 200 HTTP status code
        """
        twitter_refresh_url = "https://api.twitter.com/2/oauth2/token"

        # https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        refresh_token_response = requests.post(twitter_refresh_url,
                                               headers={"Content-Type": "application/x-www-form-urlencoded"},
                                               data={
                                                   "refresh_token": refresh_token,
                                                   "grant_type": "refresh_token",
                                                   "client_id": self.client_id
                                               })

        if refresh_token_response.status_code == 200:
            self.set_access_token(refresh_token_response.json()['access_token'])
            api._auth = authlib.integrations.requests_client.OAuth2Auth(
                token={"access_token": refresh_token_response.json()['access_token'], "token_type": "Bearer"}
            )
            self.get_me(return_json=True)
        else:
            raise pytwitter.PyTwitterError(f"Token refresh returned status code '{refresh_token_response.status_code}'")
        return refresh_token_response.json()

    @staticmethod
    def _parse_response(resp: requests.Response) -> dict:
        """
        Overrides default pytwitter.Api behavior to raise more expressive exceptions.
        :param resp: Response
        :return: json data
        :raises WrappedPyTwitterAPIRateLimitExceededException: If the request exceeded rate limits. Caller needs to wait
        :raises WrappedPyTwitterAPIUnauthorizedException: If the request was not authorized. Could be access token has expired
        :raises PyTwitterError: Any other exceptional or error response
        """

        try:
            data = resp.json()
        except ValueError:
            raise pytwitter.PyTwitterError(f"Unknown error: {resp.content}")

        if resp.status_code == 429:
            raise WrappedPyTwitterAPIRateLimitExceededException(resp.json())
        elif resp.status_code == 401:
            raise WrappedPyTwitterAPIUnauthorizedException(resp.json())
        elif not resp.ok:
            raise pytwitter.PyTwitterError(data)

        # note:
        # If only errors will raise
        if "errors" in data and len(data.keys()) == 1:
            raise pytwitter.PyTwitterError(data["errors"])

        # v1 token not
        if "reason" in data:
            raise pytwitter.PyTwitterError(data)

        return data


if TWITTER_CLIENT_ID is None:
    print("TWITTER_CLIENT_ID environment var not set")
    sys.exit(-1)

archive = dict()

api = WrappedPyTwitterAPI(client_id=TWITTER_CLIENT_ID, oauth_flow=True, scopes=twitter_api_scopes)
auth_details = api.OAuth2AuthenticationFlowHelper(local_ports_to_try=LOCAL_HTTPD_SERVER_PORTS_TO_TRY)

# Get details about the account. Specifically the Twitter ID for the user that authorized the app.
twitter_me = api.get_me(return_json=True)
my_twitter_id = twitter_me["data"]["id"]


# Get the list of accounts you are following
follows_rate_limit_window_seconds = 900
pagination_token = None
accounts_being_followed = []
with open("twitter_followers_endpoint_response_schema.json") as response_schema_file:
    followers_json_schema = json.load(response_schema_file)

while True:
    try:
        following_query_result = api.get_following(user_id=my_twitter_id,
                                                   return_json=True,
                                                   pagination_token=pagination_token)

        jsonschema.validate(following_query_result, followers_json_schema)

        accounts_being_followed = accounts_being_followed + following_query_result['data']

        if 'next_token' not in following_query_result['meta'].keys():
            break

        pagination_token = following_query_result['meta']['next_token']

    except WrappedPyTwitterAPIUnauthorizedException:
        logging.info("Authentication failed. Access token may have expired")
        # To refresh temporary access token "offline.access" MUST be one of the requested scopes in construction of
        # API object
        auth_details = api.refresh_access_token(auth_details["refresh_token"])
        continue
    except WrappedPyTwitterAPIRateLimitExceededException:
        logging.info(f"Follows Twitter user rate limit exceeded. Waiting {follows_rate_limit_window_seconds} seconds.")
        time.sleep(follows_rate_limit_window_seconds)
        continue
    except pytwitter.error.PyTwitterError as ptw:
        logging.fatal("PyTwitterError with unknown message format '{}'".format(ptw.message['status'], ptw.message))
        break

missed_id = None

for account_being_followed in accounts_being_followed:
    try:
        if missed_id is not None:
            api.unfollow_user(user_id=my_twitter_id, target_user_id=missed_id)
            missed_id = None

        api.unfollow_user(user_id=my_twitter_id, target_user_id=account_being_followed["id"])
    except WrappedPyTwitterAPIUnauthorizedException:
        logging.info("Authentication failed. Access token may have expired")
        # To refresh temporary access token "offline.access" MUST be one of the requested scopes in construction of
        # API object
        auth_details = api.refresh_access_token(auth_details["refresh_token"])
        missed_id=account_being_followed["id"]
        continue
    except WrappedPyTwitterAPIRateLimitExceededException:
        logging.info(f"Follows Twitter user rate limit exceeded. Waiting {follows_rate_limit_window_seconds} seconds.")
        missed_id=account_being_followed["id"]
        time.sleep(follows_rate_limit_window_seconds)
        continue
    except pytwitter.error.PyTwitterError as ptw:
        logging.fatal("PyTwitterError with unknown message format '{}'".format(ptw.message['status'], ptw.message))
        break
