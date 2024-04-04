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




route_dictionary_CLIregex = {}

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
    route_dictionary_CLIregex[network] = route_info


print('\nComplete route dictionary:')
pprint(route_dictionary_CLIregex)  

'''
{'0.0.0.0/0': {'admin_distance': '1',
               'description': 'N/A',
               'interface': '',
               'metric': '0',
               'next_hop': 'N/A',
               'protocol': 'S'},
 '10.0.0.0/24': {'admin_distance': '0',
                 'description': 'directly connected,',
                 'interface': 'Loopback0',
                 'metric': 'N/A',
                 'next_hop': 'N/A',
                 'protocol': 'C'},
 '10.0.0.1/32': {'admin_distance': '0',
                 'description': 'Local interface',
                 'interface': 'Loopback0',
                 'metric': 'N/A',
                 'next_hop': 'N/A',
                 'protocol': 'L'},
 '192.168.1.0/24': {'admin_distance': '0',
                    'description': 'directly connected,',
                    'interface': 'GigabitEthernet0/0',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'C'},
 '192.168.1.1/32': {'admin_distance': '0',
                    'description': 'Local interface',
                    'interface': 'GigabitEthernet0/0',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'L'},
 '192.168.2.0/24': {'admin_distance': '0',
                    'description': 'directly connected,',
                    'interface': 'GigabitEthernet0/1',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'C'},
 '192.168.2.1/32': {'admin_distance': '0',
                    'description': 'Local interface',
                    'interface': 'GigabitEthernet0/1',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'L'},
 '192.168.3.0/24': {'admin_distance': '0',
                    'description': 'directly connected,',
                    'interface': 'GigabitEthernet0/2',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'C'},
 '192.168.3.1/32': {'admin_distance': '0',
                    'description': 'Local interface',
                    'interface': 'GigabitEthernet0/2',
                    'metric': 'N/A',
                    'next_hop': 'N/A',
                    'protocol': 'L'},
 '192.168.5.0/24': {'admin_distance': '120',
                    'description': 'N/A',
                    'interface': 'GigabitEthernet0/2',
                    'metric': '1',
                    'next_hop': '192.168.3.2',
                    'protocol': 'R'}}
'''

# Now you can print the route information using the network as the key
for network, info in route_dictionary_CLIregex.items():
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
    
for network in route_dictionary_CLIregex.keys():
    # print('for network in route_dictionary.keys():')
    # pprint(device.get_route_to(network))

    print('for network in route_dictionary.keys():')
    
    # Get route information for the specific network
    route_info = device.get_route_to(network)
    
    # Store the route information in the all_routes_info dictionary
    all_routes_info[network] = route_info
    
    # Print the route information for this network
    pprint(route_info)

######### ACCESSING NESTED DICTIONARY
    
print('dictionary: all_routes_info')
pprint(all_routes_info)
print("\n")


print("dictionary: One of the keys in all_routes_info['192.168.5.0/24']")
print(all_routes_info['192.168.5.0/24'])

print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['current_active'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['last_active'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['next_hop'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['outgoing_interface'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['preference'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['protocol'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['protocol_attributes'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['routing_table'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][0]['selected_next_hop'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['age'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['current_active'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['last_active'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['next_hop'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['outgoing_interface'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['preference'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['protocol'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['protocol_attributes'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['routing_table'])
print(all_routes_info['192.168.5.0/24']['192.168.5.0/24'][1]['selected_next_hop'])

######### END OF NEW CODE


# all_routes_info is your nested dictionary

# Iterate through each network in the dictionary
for network, routes_info in all_routes_info.items():
    # Now, routes_info is the dictionary with route details list
    
    #print('ALL_ROUTES_INFO[NETWORK]:', all_routes_info[network])
    print("dictionary: One of the keys, network (192.168.5.0/24) in all_routes_info.items()")
    print("all_routes_info['192.168.5.0/24']")
    print(all_routes_info['192.168.5.0/24'])   
    
    # Iterate through each route detail dictionary in the list
    for route_detail in routes_info[network]:  # as each key corresponds to a list of dictionaries
        print(f"Network: {network}")
        
        # Now print each key-value pair in the route detail
        for key, value in route_detail.items():
            print(f"  {key}: {value}")
            
        print(f"    Specific detail - Outgoing Interface: {route_detail['outgoing_interface']}")        
        
        print()  # Print a newline for better readability between each route detail
