import routing_table_napalm

#from napalm import get_network_driver
import napalm
from pprint import pprint


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
for destination, details in route_info.items():
    
    # Since details is a list (as per the structure of route_info), 
    # details[0] accesses the first and only element in this list.
    # detail is then set to this first item, which is a dictionary containing the routing details for that specific destination.
    detail = details[0]
    
    # Each of the following lines extracts a specific piece of information from the detail dictionary 
    # and assigns it to a corresponding variable: 
    # age = detail['age']: Retrieves the 'age' of the route, which could indicate how long ago the route was updated.
    age = detail['age']
    current_active = detail['current_active']
    last_active = detail['last_active']
    next_hop = detail['next_hop']
    outgoing_interface = detail['outgoing_interface']
    preference = detail['preference']
    protocol = detail['protocol']
    protocol_attributes = detail['protocol_attributes']
    routing_table = detail['routing_table']
    selected_next_hop = detail['selected_next_hop']

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


