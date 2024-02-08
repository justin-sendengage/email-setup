import requests
from tld import get_fld
import sys

# Command-line arguments for domain, hostname, and ip_address
if len(sys.argv) != 4:
    print("Usage: python create_dns_cloudflare.py <domain> <hostname> <ip_address>")
    sys.exit(1)

domain = sys.argv[1]  # Domain to add DNS records to
hostname = sys.argv[2]  # Hostname for the MX record
ip_address = sys.argv[3]  # IP address for the SPF record

# Replace these variables with your own data
api_key = os.getenv('MY_API_KEY')
email = os.getenv('MY_EMAIL_ADDRESS')

# Cloudflare API endpoint to list all zones
zones_url = 'https://api.cloudflare.com/client/v4/zones'

headers = {
    'X-Auth-Email': email,
    'X-Auth-Key': api_key,
    'Content-Type': 'application/json',
}

def get_root_domain(domain):
    # Use the tld library to get the root domain from a given domain
    return get_fld(domain, fix_protocol=True)

def add_dns_record(zone_id, type, name, content, ttl=1, priority=None):
    dns_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    dns_data = {
        'type': type,
        'name': name,
        'content': content,
        'ttl': ttl,
    }
    if priority is not None:
        dns_data['priority'] = priority

    response = requests.post(dns_url, headers=headers, json=dns_data)
    if response.status_code == 200:
        print(f"Successfully added {type} record for {name} with auto TTL")
    else:
        print(f"Failed to add {type} record for {name}. Status code: {response.status_code}")

# Determine the root domain from the provided domain
root_domain = get_root_domain(domain)

# Step 1: Find the Zone ID for the root domain
response = requests.get(zones_url, headers=headers)
if response.status_code == 200:
    zones = response.json()['result']
    zone_id = next((zone['id'] for zone in zones if zone['name'] == root_domain), None)
    if zone_id:
        print(f"Found Zone ID for root domain {root_domain}: {zone_id}")
        # Step 2: Insert MX, DMARC, and SPF records for the (sub)domain
        add_dns_record(zone_id, 'MX', domain, hostname, priority=10)
        dmarc_record_name = '_dmarc.' + domain
        add_dns_record(zone_id, 'TXT', dmarc_record_name, f'v=DMARC1; p=reject; rua=mailto:dmarc@{root_domain}; pct=100')
        add_dns_record(zone_id, 'TXT', domain, f'v=spf1 ip4:{ip_address} -all')
    else:
        print(f"Root domain {root_domain} not found in your Cloudflare account.")
else:
    print(f'Failed to retrieve zones. Status code: {response.status_code}')
