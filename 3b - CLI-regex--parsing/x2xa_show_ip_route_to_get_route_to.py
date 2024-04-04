from napalm import get_network_driver
from pprint import pprint
import re

# Replace with your device's details
hostname = "192.168.1.1"
username = "admin"
password = "cisco"

# Define the driver for Cisco IOS
driver = get_network_driver('ios')
device = driver(hostname, username, password)

# Open the connection to the device
device.open()

# Execute your code here
'''
(?P<protocol>[A-KM-Z]\*?): This named capturing group now matches a single uppercase letter ([A-KM-Z], excluding 'L') followed by an optional asterisk (\*?). The asterisk is escaped with a backslash because it's a special character in regular expressions. The ? makes the asterisk optional, allowing the regex to match both regular protocol identifiers and the S* notation.
'''
route_regex = re.compile(r'^(?P<protocol>[A-KM-Z]\*?)\s+(?P<destination>\S+)')

output = device.cli(["show ip route"])
routing_table_raw = output["show ip route"]
print(routing_table_raw)  # Debug: Check the raw output

# Parse the output and build the list of destinations
destinations = set()
for line in routing_table_raw.splitlines():
    match = route_regex.search(line)
    if match:
        protocol = match.group('protocol')
        destination = match.group('destination')
        destinations.add(destination)

# Get detailed route information for each destination
detailed_routing_table = {}
for destination in destinations:
    route_details = device.get_route_to(destination=destination)
    detailed_routing_table[destination] = route_details

print('\n')
# Display the detailed routing table
pprint(detailed_routing_table)





# Close the connection to the device
device.close()
