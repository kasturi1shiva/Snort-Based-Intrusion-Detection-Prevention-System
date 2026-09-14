#!/usr/bin/env python3
import ipaddress
import os
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LOCAL_FEED = BASE / "feeds" / "blocked-ips.txt"
ALLOWLIST = BASE / "feeds" / "allowlist.txt"
OUTPUT = BASE / "rules" / "blocked-ips.rules"

def parse_ips(text):
    result = set()
    for line in text.splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        try:
            ip = ipaddress.ip_address(value)
            if ip.version == 4:
                result.add(str(ip))
        except ValueError:
            continue
    return result

blocked = parse_ips(LOCAL_FEED.read_text())
allow = parse_ips(ALLOWLIST.read_text())

url = os.getenv("BLOCKLIST_URL", "").strip()
if url:
    request = urllib.request.Request(url, headers={"User-Agent": "Snort-Lab-Threat-Intel-Updater/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        blocked |= parse_ips(response.read().decode("utf-8", errors="ignore"))

blocked -= allow

if not blocked:
    raise SystemExit("No valid IPv4 blocklist entries available.")

ordered = sorted(blocked, key=lambda x: tuple(int(v) for v in x.split(".")))
ip_list = ",".join(ordered)
home_net = os.getenv("HOME_NET", "192.168.56.20/32")

OUTPUT.write_text(
    f'ipvar BLOCKED_IPS [{ip_list}]\n'
    f'drop ip $BLOCKED_IPS any -> {home_net} any (msg:"THREAT INTEL BLOCKED SOURCE"; sid:9000001; rev:1;)\n',
    encoding="utf-8"
)

print(f"Generated {OUTPUT} with {len(blocked)} IPv4 entries.")
