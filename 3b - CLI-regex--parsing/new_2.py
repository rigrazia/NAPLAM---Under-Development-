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
route_regex = re.compile(r'^(?:(?P<protocol>[A-Z]\*?)\s+(?P<destination>\S+))|(?:(?P<metrics>\[\d+/\d+\])\s+via\s+(?P<next_hop>\S+))')


#output = device.cli(["show ip route"])
#routing_table_raw = output["show ip route"]
routing_table_raw = ios_output
print(routing_table_raw)  # Debug: Check the raw output

# Parsing the output and building the routing table
routing_table = {}
current_destination = None
for line in routing_table_raw.splitlines():
    match = route_regex.search(line)
    if match:
        if match.group('destination'):
            # This is a new primary route
            current_destination = match.group('destination')
            routing_table[current_destination] = [{
                'protocol': match.group('protocol'),
                'metrics': match.group('metrics'),
                'next_hop': match.group('next_hop')
            }]
        elif match.group('metrics') and current_destination:
            # This is an additional path for the current route
            routing_table[current_destination].append({
                'metrics': match.group('metrics'),
                'next_hop': match.group('next_hop')
            })

# Display the routing table
for destination, paths in routing_table.items():
    print(f"Destination: {destination}")
    for path in paths:
        print(f"  Path: {path}")



# Close the connection to the device
device.close()
