import os
import sys

import requests
import netaddress
import jsonschema

service_api_key_ipdata = os.environ.get("IPDATA_API_KEY")

def a_aaaa_cname_for_fqdn(fqdn):
    ripe_dns_url = f"https://stat.ripe.net/data/dns-chain/data.json?resource={fqdn}"

    ripe_dns_response_schema = {"$id": "https://example.com/person.schema.json",
                                "$schema": "https://json-schema.org/draft/2020-12/schema",
                                "title": "ripe_rpki_response",
                                "type": "object", "required": ["data"],
                                "properties":
                                    {"data":
                                         {"type": "object",
                                          "required": ["forward_nodes"]}}}

    ripe_dns_response = requests.get(ripe_dns_url)

    if ripe_dns_response.status_code != 200:
        raise Exception(
            f"RIPE api requests to {ripe_dns_url} returned status code {ripe_dns_response.status_code}. Expected 200")
    if ripe_dns_response.json() is None:
        raise Exception(f"RIPE api requests to {ripe_dns_url} did not return JSON")

    jsonschema.validate(ripe_dns_response.json(), ripe_dns_response_schema)

    return ripe_dns_response.json()["data"]["forward_nodes"]


def prefixes_for_asn(asn):
    global service_api_key_ipdata

    ipdata_asn_response_schema = {"$id": "https://example.com/person.schema.json",
                                  "$schema": "https://json-schema.org/draft/2020-12/schema",
                                  "title": "ipdata_asn_response",
                                  "type": "object", "required": ["ipv4_prefixes", "ipv6_prefixes"],
                                  "properties": {"ipv4_prefixes": {"type": "array", "items": {"type": "string"}},
                                                 "ipv6_prefixes": {"type": "array", "items": {"type": "string"}}
                                                 }}

    ipdata_asn_url = f"https://api.ipdata.co/{asn}/?api-key={service_api_key_ipdata}"
    ipdata_asn_response = requests.get(ipdata_asn_url)

    if ipdata_asn_response.status_code != 200:
        raise Exception(
            f"ipdata api request to {ipdata_asn_url} returned status code {ipdata_asn_response.status_code}. Expected 200")
    if ipdata_asn_response.json() is None:
        raise Exception(f"ipdata api request to {ipdata_asn_url} did not return JSON")

    jsonschema.validate(ipdata_asn_response.json(), ipdata_asn_response_schema)

    return ipdata_asn_response.json()["ipv4_prefixes"], ipdata_asn_response.json()["ipv6_prefixes"]


def asn_and_route_for_ip(ip_address):
    global service_api_key_ipdata

    ipdata_ip_response_schema = {"$id": "https://example.com/person.schema.json",
                                 "$schema": "https://json-schema.org/draft/2020-12/schema",
                                 "title": "ipdata_ip_response",
                                 "type": "object", "required": ["asn", "route"],
                                 "properties": {"asn": {"type": "string"}, "route": {"type": "string"}}}

    ipdata_api_url = f"https://api.ipdata.co/{ip_address}/asn?api-key={service_api_key_ipdata}"
    ipdata_ip_response = requests.get(ipdata_api_url)

    if ipdata_ip_response.status_code != 200:
        raise Exception(
            f"ipdata api request to {ipdata_api_url} returned status code {ipdata_ip_response.status_code}. Expected 200")
    if ipdata_ip_response.json() is None:
        raise Exception(f"ipdata api request to {ipdata_api_url} did not return JSON")

    jsonschema.validate(ipdata_ip_response.json(), ipdata_ip_response_schema)

    return ipdata_ip_response.json()["route"], ipdata_ip_response.json()["asn"]


def roas_for_prefix(prefix, asn):
    ripe_rpki_response_schema = {"$id": "https://example.com/person.schema.json",
                                 "$schema": "https://json-schema.org/draft/2020-12/schema",
                                 "title": "ripe_rpki_response",
                                 "type": "object", "required": ["data"],
                                 "properties":
                                     {"data":
                                          {"type": "object",
                                           "required": ["validating_roas", "status", "validator"]}}}

    ripe_rpki_url = f"https://stat.ripe.net/data/rpki-validation/data.json?resource={asn}&prefix={prefix}"

    ripe_rpki_response = requests.get(ripe_rpki_url)

    if ripe_rpki_response.status_code != 200:
        raise Exception(
            f"RIPE api requests to {ripe_rpki_url} returned status code {ripe_rpki_response.status_code}. Expected 200")
    if ripe_rpki_response.json() is None:
        raise Exception(f"RIPE api requests to {ripe_rpki_url} did not return JSON")

    jsonschema.validate(ripe_rpki_response.json(), ripe_rpki_response_schema)

    return ripe_rpki_response.json()["data"]["status"], ripe_rpki_response.json()["data"]["validating_roas"], \
           ripe_rpki_response.json()["data"]["validator"]


if service_api_key_ipdata is None:
    print("IPDATA_API_KEY env variable not set")
    sys.exit(-1)

for query_ip in ["82.21.211.1", "181.189.100.1", "37.72.140.1", "177.131.135.1"]:
    route, asn = asn_and_route_for_ip(query_ip)
    status, validating_roas, validator = roas_for_prefix(route, asn)
    print(f"\t{query_ip} => {asn} {route} -> ROA {status}")

"""
try:
    a_aaaa_cname_mappings = a_aaaa_cname_for_fqdn("twitter.com")
    for query_fqdn, query_ips in a_aaaa_cname_mappings.items():
        print(f"{query_fqdn}")
        for query_ip in query_ips:
            route, asn = asn_and_route_for_ip(query_ip)
            status, validating_roas, validator = roas_for_prefix(route, asn)
            print(f"\t{query_ip} => {asn} {route} -> ROA {status}")
except Exception as e:
    print(e)
    sys.exit(-1)
"""