import os
import sys

import requests

data = {"status": "Hello world from API"}

mastodon_host = "notpickard.com"
mastodon_api_status_url = f"https://{mastodon_host}/api/v1/statuses"
mastodon_api_bearer_token = os.getenv("mastodon_api_bearer_token")

if mastodon_api_bearer_token is None:
    print("no bearer token")
    sys.exit(-1)

r = requests.post(mastodon_api_status_url, data=data,
                  headers={'Authorization': 'Bearer %s' % (mastodon_api_bearer_token)})
json_data = r.json()  # you can inspect the json response to check for problems
