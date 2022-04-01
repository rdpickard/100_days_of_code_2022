import json

from ripe.atlas.sagan import DnsResult
import requests

with open("../local/day_24/RIPE-Atlas-measurement-39889130.json") as dnsresultjsonfile:
    dnsresultjson = json.load(dnsresultjsonfile)

probe_cache = dict()

for dns_result_json in dnsresultjson:

    dns_result = DnsResult(dns_result_json)
    for response in dns_result.responses:

        if dns_result.probe_id not in probe_cache.keys():
            probe_cache[dns_result.probe_id] = requests.get(f"https://atlas.ripe.net:443/api/v2/probes/{dns_result.probe_id}/").json()

        print(f"{probe_cache[dns_result.probe_id]['country_code']} {dns_result.origin} -> {response.destination_address}")

        if response.abuf is None:
            continue
        for answer in response.abuf.answers:
            print("{}".format(answer))