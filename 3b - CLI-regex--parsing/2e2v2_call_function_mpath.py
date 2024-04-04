import napalm
from pprint import pprint
import routing_table_napalm


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
# routing_table_raw = output["show ip route"]
# print(routing_table_raw)  # Debug: Check the raw output

# Use show_ip_route_napalm.show_ip_route() to get routing table as a dictionary
route_info = routing_table_napalm.show_ip_route(device)
pprint(route_info)

# See show_ip_route for type of data returned
'''
'192.168.2.0/24': [{'age': '',
                     'current_active': True,
                     'inactive_reason': '',
                     'last_active': True,
                     'next_hop': '',
                     'outgoing_interface': 'GigabitEthernet0/1',
                     'preference': 0,
                     'protocol': 'connected',
                     'protocol_attributes': {},
                     'routing_table': 'default',
                     'selected_next_hop': True}],
 '192.168.3.0/24': [{'age': 3,
                     'current_active': True,
                     'inactive_reason': '',
                     'last_active': True,
                     'next_hop': '192.168.2.2',
                     'outgoing_interface': 'GigabitEthernet0/1',
                     'preference': 1,
                     'protocol': 'rip',
                     'protocol_attributes': {},
                     'routing_table': 'default',
                     'selected_next_hop': True}],
'''

# route_info is a dictionary. The method .items() is used to iterate over this dictionary.
# Each iteration of the loop gives you a key-value pair: destination and details.
#    destination is the key in the route_info dictionary, 
#       typically representing a network destination like an IP address or subnet.
#    details is the value associated with that key in route_info. 
#       In your context, it is a list of dictionaries where each dictionary 
#       contains routing information related to that destination.
for destination, details_list in route_info.items():
    
    # Iterate over all entries in the details_list LIST:
    # WAS detail = details[0]
    # When there are multiple routing entries for a destination, such as in the case of equal cost load balancing, you need to modify the code to handle multiple details per destination. 
    # Instead of just taking the first entry (details[0]), you should iterate over all entries in the details list. 
    # for detail in details: iterates over each entry in the details list for the current destination. 
    #      This allows you to process all routing entries for each destination.
    for detail_dictionary in details_list:
    
        # Extract the relevant information from each detail. 
        # If there are multiple routes for a destination, this loop will process each of them in turn.
        # Each of the following lines extracts a specific piece of information from the detail dictionary 
        # and assigns it to a corresponding variable: 
        # age = detail['age']: Retrieves the 'age' of the route, which could indicate how long ago the route was updated.
        age = detail_dictionary['age']
        current_active = detail_dictionary['current_active']
        last_active = detail_dictionary['last_active']
        next_hop = detail_dictionary['next_hop']
        outgoing_interface = detail_dictionary['outgoing_interface']
        preference = detail_dictionary['preference']
        protocol = detail_dictionary['protocol']
        protocol_attributes = detail_dictionary['protocol_attributes']
        routing_table = detail_dictionary['routing_table']
        selected_next_hop = detail_dictionary['selected_next_hop']

        #print(f"Destination: {destination}\n  Age: {age}\n  Current Active: {current_active}\n  Last Active: {last_active} ")

        print("\n")
        print("Destination:", destination)
        print("\tAge:", age)
        print("\tCurrent Active:", current_active)
        print("\tLast Active:", last_active)
        print("\tNext Hop:", next_hop)
        print("\tOutgoing Interface:", outgoing_interface)
        print("\tPreference:", preference)
        print("\tProtocol:", protocol)
        print("\tProtocol Attributes:", protocol_attributes)
        print("\tRouting Table:", routing_table)
        print("\tSelected Next Hop:", selected_next_hop)         



# Close the connection to the device
device.close()

'''
fruits = {
    'apple': 'red',
    'banana': 'yellow',
    'grape': 'purple'
}

# Iterate over the dictionary
for fruit, color in fruits.items():
    print(f"The color of {fruit} is {color}.")

# Iterate over the keys of the dictionary
for fruit in fruits.keys():
    # Use the key to access the corresponding value
    color = fruits[fruit]
    print(f"The color of {fruit} is {color}.")

'''
