# Detection and Prevention Validation

| Test | IDS Expected | IPS Expected |
|---|---|---|
| ICMP Echo | Alert | Drop when ICMP IPS rule is enabled |
| TCP/22 SYN | Alert | Drop when SSH IPS rule is enabled |
| TCP/23 SYN | Alert if matching detection exists | Drop |
| TCP/3389 SYN | Alert if matching detection exists | Drop |
| Blocklist IP | Alert/Drop according to rule | Drop |
| Allowlisted IP | No blocklist drop | No blocklist drop |

## Validation Checklist

- Snort configuration test passes
- Rules load without errors
- Attacker traffic reaches the inspection interface
- IDS alerts contain correct source and destination
- Wireshark confirms corresponding packets
- Threat-intelligence feed updates successfully
- Allowlist filtering works
- IPS rules are tested after IDS validation
- Blocked connections fail as expected
- Detection thresholds are tuned
- Evidence is stored for each test
