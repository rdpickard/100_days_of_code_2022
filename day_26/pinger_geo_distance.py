import json
import os
import sys

from ripe.atlas.sagan import DnsResult, PingResult
import requests
from geopy import distance

atlas_job_id = 39945669

atlas_api_call_url = f"https://atlas.ripe.net/api/v2/measurements/{atlas_job_id}/results/"
atlas_api_response = requests.get(f"https://atlas.ripe.net/api/v2/measurements/{atlas_job_id}/results/",
                                 params={"key": os.environ.get("ATLAS_API_KEY")})

ping_results_json = None

if atlas_api_response.status_code == 200:
    ping_results_json = atlas_api_response.json()
elif atlas_api_response.status_code != 200:
    print(f"API call to RIPE Atlas '{atlas_api_call_url}' returned response code {atlas_api_response.status_code}. Expected 200. Exiting")
    sys.exit(-1)
elif atlas_api_response.json() is None:
    print(f"API call to RIPE Atlas '{atlas_api_call_url}' did not return JSON. Exiting")
    sys.exit(-1)

probe_cache = dict()

for ping_results_from_probe in ping_results_json:

    ping_result = PingResult(ping_results_from_probe)

    if ping_result.probe_id not in probe_cache.keys():
        probe_cache[ping_result.probe_id] = requests.get(
            f"https://atlas.ripe.net:443/api/v2/probes/{ping_result.probe_id}/").json()

    probe_cache[ping_result.probe_id]["rtt_min"] = ping_result.rtt_min

miles_per_millisecond_at_c = 186

for probe_id, probe_details in probe_cache.items():
    miles_miles = probe_details["rtt_min"] / 2 * miles_per_millisecond_at_c
    print(f"from #{probe_id} {probe_details['country_code']} ->  {miles_miles} ({probe_details['rtt_min']/2})")
    for other_probes_id, other_probes_details in probe_cache.items():
        if other_probes_id == probe_id:
            continue
        try:
            probes_miles_apart = distance.distance(probe_details["geometry"]["coordinates"], other_probes_details["geometry"]["coordinates"]).miles
            print(f"\tmiles {probes_miles_apart} from #{other_probes_id} {other_probes_details['country_code']}")
        except ValueError:
            print(f'\t err with #{other_probes_id}  {other_probes_details["geometry"]["coordinates"]}')

