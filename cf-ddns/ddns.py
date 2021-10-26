import json
import requests
from config import email, domain, global_key


def setup_info():
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": global_key,
    }
    api = "https://api.cloudflare.com/client/v4/zones/"
    r = requests.get(api, headers=headers).json()
    zone = r["result"][0]["id"]
    r = requests.get(f"{api}{zone}/dns_records", headers=headers).json()
    dns_records = [_ for _ in r["result"] if _["name"] == domain][0]["id"]
    return {
        "zone": zone,
        "dns_records": dns_records,
    }


def ddns_request(ipv6, zone, dns_records):
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": global_key,
    }
    dns_info = {
        "type": "AAAA",
        "name": domain,
        "content": ipv6,
        "ttl": 60,
        "proxied": False,
    }
    data = json.dumps(dns_info)
    api = "https://api.cloudflare.com/client/v4/zones"
    url = f"{api}/{zone}/dns_records/{dns_records}"
    r = requests.put(url, data=data, headers=headers)
    if r.status_code == 200:
        print(f"Domain: {domain} Success!")
    else:
        print(f"{domain}: Fail!")


if __name__ == "__main__":
    user_info = setup_info()
    zone = user_info["zone"]
    dns_records = user_info["dns_records"]
    ipv6 = requests.get("http://ipv6.icanhazip.com").text.strip()
    print(f"Current IP: {ipv6}")
    ddns_request(ipv6, zone, dns_records)
