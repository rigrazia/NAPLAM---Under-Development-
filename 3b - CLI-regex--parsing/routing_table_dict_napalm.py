import re

def show_ip_route(device):

    '''
    (?P<protocol>[A-KM-Z]\*?): This named capturing group now matches a single uppercase letter ([A-KM-Z], excluding 'L') followed by an optional asterisk (\*?). The asterisk is escaped with a backslash because it's a special character in regular expressions. The ? makes the asterisk optional, allowing the regex to match both regular protocol identifiers and the S* notation.
    '''
    route_regex = re.compile(r'^(?P<protocol>[A-KM-Z]\*?)\s+(?P<destination>\S+)')

    '''
    In essence, the following code segment is extracting unique network destinations from the raw output of a routing table, using regular expressions to parse each line. The resulting set, destinations, contains each unique network destination found in the routing table.
    '''

    # The cli method is used to execute CLI commands on the network device. 
    # The entire output from the cli method is stored in the variable output. 
    # output is a dictionary: key is 'show ip route' and value is 'all the output as a string'
    output = device.cli(["show ip route"])

    # Retrieving and Printing the Raw Routing Table:
    # output is assigned just the value, the string, of the the cli-output (no key of 'show ip route')
    routing_table_raw = output["show ip route"]
    print(routing_table_raw)  # Debug: Check the raw output


    # Parse the output and build the list of destinations
    # A set named destinations is initialized. 
    # Sets are collections in Python that automatically remove duplicate entries. 
    # This will be used to store unique network destinations extracted from the routing table.
    destinations = set()

    # Iterating Over Each Line of the Raw Routing Table:
    # The splitlines() method splits the routing_table_raw string into a list of individual lines. 
    # This is useful because routing tables typically present one route per line.
    for line in routing_table_raw.splitlines():
        
        # Applying the Regular Expression to Each Line:
        # For each line, the script uses a regular expression (route_regex) to search for specific patterns. 
        # This regular expression is designed to identify and capture parts of the line that represent the routing protocol and the destination network.
        match = route_regex.search(line)
        
        # Checking for a Match and Extracting Information:
        # If match is true - regex found a matching pattern in routing_table_raw
        # checks whether the regular expression found a pattern in the line. 
        # If match is not None (meaning a pattern was found), the block of code under this if statement is executed.
        if match:
            
            # Extracts the captured parts of the line corresponding to the routing protocol and destination network, respectively.
            protocol = match.group('protocol')
            destination = match.group('destination')
            
            # Adding Unique Destinations to the Set:
            # The destination extracted from each line is added to the destinations set. 
            # If the same destination appears in multiple lines of the routing table, it will only be stored once in the set, thanks to the nature of sets in Python.
            destinations.add(destination)

    # Get detailed route information for each destination
    # Initialize an Empty Dictionary:
    detailed_routing_table = {}

    # Iterate Over Each Destination: 
    # Iterates over each element in the destinations set. Each element in this set represents a network destination (e.g., an IP address or a network segment) that was previously extracted from the routing table.
    for destination in destinations:
        
        # Retrieve Routing Details:
        # This method is part of the napalm library, and it is used to retrieve detailed routing information for the specified destination. The destination variable holds the current destination from the destinations set. The route_details variable will receive the routing information returned by this method. Typically, this information includes various attributes of the route, like the next hop, the age of the route, the protocol used, etc.
        route_details = device.get_route_to(destination=destination)
        
        # Store Routing Details in the Dictionary:
        # This line stores the retrieved routing details in the detailed_routing_table dictionary. The key for each entry in the dictionary is the destination, and the value is the corresponding routing details for that destination. It is assumed that route_details is a dictionary with the destination as a key, and the information is extracted from it.The expression route_details[destination] accesses the routing information specific to the current destination within the route_details dictionary. This information is then assigned to the corresponding key in detailed_routing_table
        detailed_routing_table[destination] = route_details[destination]

    print('\n')
    # Display the detailed routing table
    return(detailed_routing_table)


    # Close the connection to the device
    #device.close()


'''
Returns dictionary with:
KEY for each destination: [ ONE ITEM LIST WITH A DICTIONARY OF KEY-VALUE PAIRS
        { 'key': value,
          'key': value,
          etc
        },
KEY for each destination: [ ONE ITEM LIST WITH A DICTIONARY OF KEY-VALUE PAIRS
        { 'key': value,
          'key': value,
          etc
        }
]

{'0.0.0.0/0': [{'age': '',
                'current_active': True,
                'inactive_reason': '',
                'last_active': True,
                'next_hop': '192.168.2.2',
                'outgoing_interface': '',
                'preference': 0,
                'protocol': 'static',
                'protocol_attributes': {},
                'routing_table': 'default',
                'selected_next_hop': True}],
 '192.168.1.0/24': [{'age': '',
                     'current_active': True,
                     'inactive_reason': '',
                     'last_active': True,
                     'next_hop': '',
                     'outgoing_interface': 'GigabitEthernet0/0',
                     'preference': 0,
                     'protocol': 'connected',
                     'protocol_attributes': {},
                     'routing_table': 'default',
                     'selected_next_hop': True}],
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
 '192.168.4.0/24': [{'age': 2,
                     'current_active': True,
                     'inactive_reason': '',
                     'last_active': True,
                     'next_hop': '192.168.2.2',
                     'outgoing_interface': 'GigabitEthernet0/1',
                     'preference': 1,
                     'protocol': 'rip',
                     'protocol_attributes': {},
'''