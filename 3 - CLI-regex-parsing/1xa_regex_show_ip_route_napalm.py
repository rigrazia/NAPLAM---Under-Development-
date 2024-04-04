import napalm
import re
from pprint import pprint

# Define the driver for Cisco IOS
driver = napalm.get_network_driver('ios')

# Device details
device = driver( hostname='192.168.1.1', 
                 username='admin',
                 password='cisco',
                 optional_args={'secret':'class'} )


# Open the connection to the device
device.open()




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



output = device.cli(["show ip route"])   # dictionary['key']
print('output:', type(output))
print('output:', output)


routing_table_raw = output["show ip route"]      # string_var = dictionary['key']

print(routing_table_raw)  # Debug: Check the raw output





routes = route_regex.findall(routing_table_raw)




route_dictionary = {}

# Process the results
for route in routes:
    
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

# Initialize an empty dictionary to hold all route information
all_routes_info = {}
    
for network in route_dictionary.keys():
    # print('for network in route_dictionary.keys():')
    # pprint(device.get_route_to(network))

    print('for network in route_dictionary.keys():')
    
    # Get route information for the specific network
    route_info = device.get_route_to(network)
    
    # Store the route information in the all_routes_info dictionary
    all_routes_info[network] = route_info
    
    # Print the route information for this network
    pprint(route_info)
    
print("Complete Route Information for All Networks:")
pprint(all_routes_info)

