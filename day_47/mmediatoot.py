import os
import pathlib
import sys

import requests
from pathlib import Path

mastodon_host = "notpickard.com"
mastodon_api_status_url = f"https://{mastodon_host}/api/v1/statuses"
mastodon_api_media_url = f"https://{mastodon_host}/api/v1/media"
mastodon_api_bearer_token = os.getenv("mastodon_api_bearer_token")

image_file_path = "./media/peakperformance.jpg"

media_response = requests.post(mastodon_api_media_url,
                               files={'file': ("peakperformance.jpg", pathlib.Path(image_file_path).open('rb'),
                                               'application/octet-stream')},
                               headers={'Authorization': 'Bearer %s' % mastodon_api_bearer_token})
if media_response.status_code != 200:
    print(
        f"media api request to '{mastodon_api_media_url}' returned status {media_response.status_code}. Expected 200. Exiting")
    sys.exit(-1)
if media_response.json() is None:
    print(f"media api request to '{mastodon_api_media_url}' Did not return JSON. Exiting")
    sys.exit(-1)
if "id" not in media_response.json():
    print(f"media api request to '{mastodon_api_media_url}' Did not return JSON with required key 'id'. Exiting")
    sys.exit(-1)

toot_response = requests.post(mastodon_api_status_url,
                              data={
                                  "status": "This is Peak Performance. From API test",
                                  "media_ids[]": media_response.json()["id"]
                              },
                              headers={'Authorization': 'Bearer %s' % mastodon_api_bearer_token})
if toot_response.status_code != 200:
    print(f"Status api request to {mastodon_api_status_url} returned status {media_response.status_code}. Expected 200. Exiting")
    sys.exit(-1)
#json_data = r.json()
