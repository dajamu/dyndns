# DynDNS
Scripts to use the IONOS API for updating DNS records.

# Usage
Create a file called dyndns.conf in the same directory as the dns.py script:
```
# Sample config file
[api]
base_url = https://api.hosting.ionos.com/dns
public_key = XXX
private_key = YYY

[general]
fqdn = host.example.com
```
Substitute in your IONOS API credentials and the FQDN that you want to track your external IP address (must be a valid FQDN for a zone that you own).

Test that the script works ok and then create a cron job for it :-)
