# Snort-Based-Intrusion-Detection-Prevention-System
## Project Overview

A two-VM network security lab implementing Snort 3 as an IDS and inline IPS on a protected Linux host. The project combines threat-intelligence IP blocklists, custom signatures, behavioral detection, rate-based controls, alert analysis, and automated blocklist updates.

## Lab Architecture

```text
+-----------------------+
| Attacker VM           |
| Security Testing Host |
| 192.168.56.10         |
+-----------+-----------+
            |
            | Lab Network
            v
+-----------+-----------+
| Protected VM          |
| Linux + Snort 3       |
| 192.168.56.20         |
| IDS + Inline IPS      |
+-----------+-----------+
            |
            v
      Protected Services
```

The protected VM is the monitored security boundary. For true inline IPS operation, traffic must traverse the Snort inspection path before reaching the protected service.

## Security Capabilities

- Threat-intelligence IP blocklist enforcement
- Local IP allowlisting
- Signature-based intrusion detection
- Inline packet dropping
- Port-scan and connection-rate detection
- ICMP reconnaissance detection
- Suspicious TCP flag detection
- HTTP request pattern detection
- DNS tunneling-style query detection
- Repeated authentication-failure detection
- Alert logging and packet investigation
- Automated blocklist refresh
- IDS-to-IPS rule validation workflow

## Repository Structure

```text
snort-enterprise-ids-ips-lab/
├── README.md
├── config/
│   └── snort.lua
├── rules/
│   ├── local.rules
│   ├── ips.rules
│   └── blocked-ips.rules
├── scripts/
│   └── update_blocklist.py
├── feeds/
│   ├── blocked-ips.txt
│   └── allowlist.txt
├── tests/
│   ├── attacker-tests.md
│   └── validation.md
├── dashboards/
│   └── incident-workflow.md
├── evidence/
├── logs/
└── LICENSE
```

## Address Plan

| System | Address | Role |
|---|---|---|
| Attacker VM | 192.168.56.10 | Controlled security testing |
| Protected VM | 192.168.56.20 | Snort IDS/IPS |
| Lab Network | 192.168.56.0/24 | Isolated environment |

Replace the addresses with your actual VM network.

## Snort Workflow

```text
Traffic
   |
   v
Preprocessing / Decode
   |
   v
Threat-Intel IP Reputation
   |
   +---- Match ----> IPS Drop
   |
   v
Custom Detection Rules
   |
   +---- Match ----> Alert / Drop
   |
   v
Logs
   |
   v
Investigation
   |
   v
Rule Tuning / Blocklist Update
```

## IDS Deployment

Validate the configuration:

```bash
sudo snort -T -c config/snort.lua
```

Run the lab rules:

```bash
sudo snort -c config/snort.lua -R rules/local.rules -i eth0 -A alert_fast
```

Use the interface connected to the lab network.

## IPS Deployment

The IPS rules use `drop` actions. Validate all signatures in IDS mode before enabling inline enforcement.

A production-style deployment requires an inline packet path and the appropriate Snort 3 DAQ configuration for the selected Linux networking design.

## Threat Intelligence Blocklist

The repository uses a generated Snort IP reputation list.

```text
feeds/blocked-ips.txt
```

The update script validates IPv4 addresses, merges an optional remote threat-intelligence feed, removes allowlisted addresses, and generates:

```text
rules/blocked-ips.rules
```

Configure an approved feed through the `BLOCKLIST_URL` environment variable.

```bash
export BLOCKLIST_URL="https://YOUR-APPROVED-FEED"
export HOME_NET="192.168.56.20/32"
python3 scripts/update_blocklist.py
```

The repository contains TEST-NET addresses only. Replace them with entries from a threat-intelligence source that you are authorized to use. Do not publish live malicious IPs in a public repository unless the feed license and your security policy permit it.

## Threat-Intelligence Pipeline

```text
External Threat Feed
        |
        v
IP Validation
        |
        v
Allowlist Filtering
        |
        v
Snort Blocklist Generation
        |
        v
IPS Enforcement
        |
        v
Alert / Log / Investigation
```

## Detection Coverage

### Reconnaissance

- TCP SYN bursts
- ICMP discovery
- Connection-rate anomalies

### Network Abuse

- Suspicious TCP flag combinations
- Repeated connection attempts
- Unauthorized service access

### Application Layer

- Suspicious HTTP request patterns
- DNS query-length anomalies

### Threat Intelligence

- Known-bad source IP matching
- Local allowlist precedence
- Generated block rules

## Testing Methodology

1. Start Snort in IDS mode.
2. Generate controlled traffic from the attacker VM.
3. Confirm alerts.
4. Capture packets with Wireshark.
5. Tune rule thresholds.
6. Validate false-positive behavior.
7. Enable the inline IPS path.
8. Repeat the same controlled tests.
9. Confirm blocked traffic.
10. Record evidence and update the incident workflow.

## Operational Metrics

Track:

- Alerts per test
- Blocked connections
- Detection latency
- False positives
- Rule hit counts
- Blocklist matches
- Protocol distribution
- Source/destination pairs

## Resume Outcomes

- Designed a two-VM network intrusion detection and prevention lab using Snort 3.
- Implemented threat-intelligence IP reputation controls with automated blocklist generation.
- Developed custom Snort signatures for reconnaissance, anomalous TCP behavior, application-layer traffic, and connection-rate anomalies.
- Configured IDS alerting and validated inline IPS packet-dropping workflows.
- Performed controlled attack simulations and correlated Snort alerts with packet captures.
- Tuned detection thresholds and maintained allowlist/blocklist controls to reduce false positives.

## Disclaimer

Use only on systems and networks you own or are explicitly authorized to test. Public threat-intelligence feeds should be used according to their licensing and acceptable-use requirements.
