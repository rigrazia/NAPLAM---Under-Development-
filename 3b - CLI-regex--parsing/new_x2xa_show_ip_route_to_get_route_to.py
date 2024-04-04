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

ios_output = '''Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, + - replicated route

Gateway of last resort is 192.168.2.2 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 192.168.2.2
      192.168.2.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.2.0/24 is directly connected, GigabitEthernet0/1
L        192.168.2.1/32 is directly connected, GigabitEthernet0/1
R     192.168.3.0/24 [120/1] via 192.168.2.2, 00:00:20, GigabitEthernet0/1
R     192.168.4.0/24 [120/1] via 192.168.2.2, 00:00:17, GigabitEthernet0/1
                     [120/1] via 192.168.5.2, 00:00:17, GigabitEthernet0/2'''

# Execute your code here
'''
(?P<protocol>[A-KM-Z]\*?): This named capturing group now matches a single uppercase letter ([A-KM-Z], excluding 'L') followed by an optional asterisk (\*?). The asterisk is escaped with a backslash because it's a special character in regular expressions. The ? makes the asterisk optional, allowing the regex to match both regular protocol identifiers and the S* notation.
'''
route_regex = re.compile(r'^(?P<protocol>[A-KM-Z]\*?)\s+(?P<destination>\S+)')

#output = device.cli(["show ip route"])
#routing_table_raw = output["show ip route"]
routing_table_raw = ios_output
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
