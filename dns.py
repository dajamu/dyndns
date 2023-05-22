#!/usr/bin/env python

import logging
import requests
import socket
import sys

from typing import Optional

api_public = "XXX"
api_private = "YYY"
base_url = "https://api.hosting.ionos.com/dns"


def add_record(
    fqdn: str,
    ipaddr: str,
    record_type: str = "A",
    ttl: int = 3600,
    prio: int = 0,
    disabled: str = "false",
) -> None:
    (_, domain) = fqdn.split(".", maxsplit=1)

    record_dict = {
        "name": fqdn,
        "type": record_type,
        "content": ipaddr,
        "ttl": ttl,
        "prio": prio,
        "disabled": disabled,
    }

    logging.debug(f"add_record: {record_dict}")
    api_patch(f"/v1/zones/{get_zone_id(domain)}", record_dict)


def api_get(endpoint: str) -> Optional[dict]:
    return requests.get(
        f"{base_url}{endpoint}",
        headers={"X-API-Key": f"{api_public}.{api_private}"},
    ).json()


def api_patch(endpoint: str, data) -> None:
    logging.debug(f"Data being sent: {data}")

    r = requests.patch(
        f"{base_url}{endpoint}",
        json=data,
        headers={
            "X-API-Key": f"{api_public}.{api_private}",
            "accept": "*/*",
            "Content-Type": "application/json",
        },
    )

    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {r.json()}")


def api_post(endpoint: str, data) -> None:
    r = requests.post(
        f"{base_url}{endpoint}",
        json=data,
        headers={
            "X-API-Key": f"{api_public}.{api_private}",
            "accept": "*/*",
            "Content-Type": "application/json",
        },
    )

    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {r.json()}")


def get_external_ip() -> str:
    try:
        ip = requests.get("https://api.myip.com").json()["ip"]
    except Exception as e:
        print("Unable to establish current public IP address.")
        sys.exit(1)

    logging.debug(f"External IP address: {ip}")
    return ip


def get_records(domain: str) -> list:
    return api_get(f"/v1/zones/{get_zone_id(domain)}")["records"]


def get_zone_id(domain: str) -> Optional[str]:
    for zone in get_zones():
        if zone["name"] == domain:
            return zone["id"]

    raise Exception(f"No zone information found for domain '{domain}'.")


def get_zones() -> list:
    return api_get("/v1/zones")


def update_a_record(fqdn: str, ipaddr: str, force: bool = False) -> bool:
    if not force:
        try:
            if socket.gethostbyname(fqdn) == ipaddr:
                print("No update required.")
                return False
        except Exception as e:
            pass

    logging.debug(f"Update to {fqdn} required.")
    add_record(fqdn, ipaddr)
    return True


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
update_a_record("home.example.com", get_external_ip())
