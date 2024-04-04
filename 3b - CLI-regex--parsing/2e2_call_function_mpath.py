import napalm
from pprint import pprint
import re


route_regex = re.compile(
    # Protocol with optional * for any route
    r'(?P<protocol>L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|U|o|P|\+|[*])\*?\s+'  
    r'(?P<network>\S+/\d+)\s+'  # Network (with CIDR notation)
    r'(?:\[(?P<admin_distance>\d+)/(?P<metric>\d+)\]\s+)?'  # Separating Administrative distance and metric
    r'(?:via\s+(?P<next_hop>\S+),\s+)?'  # Optional next-hop
    r'(?:is\s+)?(?P<description>[\w\s-]+,)?\s*'  # Description (e.g., "directly connected")
    r'(?:[0-9]{2}:[0-9]{2}:[0-9]{2},\s+)?'  # Optionally match the update time which is not needed
    r'(?P<interface>\S+)'  # Interface
)

# Replace with your device's details
hostname = "192.168.1.1"
username = "admin"
password = "cisco"

# Define the driver for Cisco IOS
# driver = get_network_driver('ios')
driver = napalm.get_network_driver('ios')
device = driver(hostname, username, password)

# Open the connection to the device
device.open()

# The cli method is used to execute CLI commands on the network device. 
# The entire output from the cli method is stored in the variable output. 
# output is a dictionary: key is 'show ip route' and value is 'all the output as a string'
output = device.cli(["show ip route"])

# Retrieving and Printing the Raw Routing Table:
# output is assigned just the value, the string, of the the cli-output (no key of 'show ip route')
routing_table_raw = output["show ip route"]
print(routing_table_raw)  # Debug: Check the raw output

routes = route_regex.findall(routing_table_raw)

route_dictionary = {}

# Process the results
for route in routes:
    '''
    route: ('R', '192.168.3.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1')
    
    in routes [('S*', '0.0.0.0/0', '1', '0', '', '', 'via'), ('C', '192.168.2.0/24', '', '', '', 'directly connected,', 'GigabitEthernet0/1'), ('L', '192.168.2.1/32', '', '', '', 'directly connected,', 'GigabitEthernet0/1'), ('R', '192.168.3.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1'), ('R', '192.168.4.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1')]  
    
    tuple unpacking. This is a convenient way to assign each element of the route tuple to a separate variable.
    
    route: This is a tuple containing all the captured groups from the regular expression for a single routing table entry. Each element in the tuple corresponds to a different part of the routing entry, as captured by the named groups in the regex. The order of elements in the route tuple corresponds to the order of the capturing groups in the regex.

    protocol, network, admin_distance, metric, next_hop, description, interface: These are the variable names to which the elements of the route tuple will be assigned. 
    Each variable is intended to hold a specific piece of information from the routing table entry:
        protocol: The protocol code (e.g., C, L, S, R, etc.).
        network: The network address and prefix length in CIDR notation.
        admin_distance: The administrative distance extracted from the routing table entry.
        metric: The metric extracted from the routing table entry.
        next_hop: The next-hop IP address if present.
        description: Any additional descriptive text or status about the route.
        interface: The interface through which the route is reachable.

    This line of code is effectively taking the matched data from one route entry, which is stored as a tuple in routes, and distributing it across several variables for easy access and readability. After this line, each of these variables holds a specific, meaningful piece of data that can be used in the subsequent code to build the route_info dictionary or for any other purpose like printing or further processing.
    '''
    
    protocol, network, admin_distance, metric, next_hop, description, interface = route


    
    # Create a nested dictionary for each route
    route_info = {
        'protocol': protocol,
        'admin_distance': admin_distance if admin_distance else '0',
        'metric': metric if metric else 'N/A',
        'next_hop': next_hop if next_hop else 'N/A',
        'description': description.strip() if description else 'N/A',
        'interface': interface
    }
    
    if route_info['interface'].strip() == 'via':
        route_info['interface'] = ''
        
    if route_info['protocol'].strip() == 'L':
        route_info['description'] = 'Local interface'
    
    # Use the network as the key for the main dictionary
    route_dictionary[network] = route_info

# Now you can print the route information using the network as the key
print('\nComplete route dictionary:')
pprint(route_dictionary)

# Now you can print the route information using the network as the key
for network, info in route_dictionary.items():
    print(f"Network: {network}")
    print(f"Protocol: {info['protocol']}, \n"
          f"Administrative Distance: {info['admin_distance']}, \n"
          f"Metric: {info['metric']}, \n"
          f"Next-Hop: {info['next_hop']}, \n"
          f"Description: {info['description']}, \n"
          f"Exit Interface: {info['interface']}")
    print()
    # print('route_dictonary:')
    # pprint(route_dictionary)
    print()