# Controlled Attacker VM Tests

Target:

```text
192.168.56.20
```

Use only the target VM in the isolated lab.

## ICMP Detection

```bash
ping -c 4 192.168.56.20
```

Expected: `LAB ICMP RECONNAISSANCE`

## Service Access

```bash
nc -vz 192.168.56.20 22
```

Expected: `LAB SSH ACCESS ATTEMPT`

## Repeated Connection Testing

```bash
for i in $(seq 1 25); do nc -z -w 1 192.168.56.20 22; done
```

Expected: `LAB TCP SYN BURST`

## Packet Capture

```bash
sudo tcpdump -ni eth0 host 192.168.56.20
```

Use Wireshark for packet-level correlation.

## IPS Validation

Enable the validated inline IPS path and test a port covered by `ips.rules`.

```bash
nc -vz 192.168.56.20 23
```

Expected: the connection is blocked when the inline IPS configuration is correctly enforcing the rule.
