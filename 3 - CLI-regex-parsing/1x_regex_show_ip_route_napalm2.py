# import routing_table_napalm

#from napalm import get_network_driver
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

'''
hostname = "192.168.1.1"
username = "admin"
password = "cisco"

device = driver(hostname, username, password)  
'''

# Open the connection to the device
device.open()



# Regular expression to match routing table entries
# Assuming routing table entries are structured as:
# Code Network/Mask [Admin/Metric] via Next-Hop, Time, Interface
# Explanation:
# \w matches any single word character (equivalent to [a-zA-Z0-9_]).
# \S+ matches a sequence of non-whitespace characters.
# \d+ matches one or more digits.
# [...] is used to capture a group of characters as a match.
# (?:...)? is a non-capturing group that makes the 'via Next-Hop' part optional, because not all entries might have a next-hop defined (like connected routes).

# (?P<protocol>[CLSRMBD]|[S]*?): This part of the pattern is for capturing the protocol. I've expanded it to include the possibility of an 'S' followed by an optional '' character. The *? is a non-greedy match for zero or one '' character. This adjustment ensures it can match both 'S' and 'S*' for static routes.
# [\w\s-]+: In the description part, I've included a dash '-' along with word characters and whitespace to ensure any descriptive text is captured correctly.
# \s+: Ensures that there are one or more whitespace characters separating each part of the entry.

# I made some groups optional using the (?:...)? pattern, such as the administrative distance/metric and next-hop. This is because these parts may not exist for all route types, especially for directly connected routes.
# The description part is used to capture any text leading up to the interface, such as "is directly connected". This part of the regex might need to be adjusted depending on the variety of route descriptions in your actual IOS outputs.
# ?P<interface>\S+ captures the interface name, which is usually at the end of the routing entry.

# re.compile() allows for efficient reuse of the regex pattern and makes the code that uses it cleaner and easier to read. Divide it into separae statements.

# Define a regex pattern to match the routing table entries

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



'''
route_regex: This is a compiled regular expression object created earlier in the code using re.compile(). It contains the pattern that defines the structure of the routing table entries you're interested in.

.findall() method: This is a method of the regex object (route_regex in this case) that searches the string passed to it (here, ios_output) for all non-overlapping matches of the regex pattern. It returns a list of the matches.

ios_output: This is the string containing the IOS routing table output that you want to search through. This string is passed as an argument to the .findall() method.

When you use route_regex.findall(ios_output), here's what happens:

The .findall() method scans the entire ios_output string from start to finish, looking for any substrings that match the route_regex pattern.
Each match found by .findall() is returned as a tuple containing all the captured groups from the regular expression. If there are no groups in the regular expression, it returns a list of strings matching the whole pattern. If there are groups, it returns a list of tuples, each tuple representing one match of the pattern, containing all the groups.
The list of matches (or tuples, in this case) is assigned to the variable routes.
In the context of your task, each tuple in the routes list corresponds to one routing table entry. The groups in the regular expression are designed to capture the relevant parts of each entry: protocol, network address and prefix length, administrative distance/metric, next-hop, and exit interface. This means each tuple will hold these parts as elements, allowing you to easily access and process each aspect of the routing table entries as demonstrated when the code iterates through routes and prints out the formatted results.

Using findall() is a powerful way to extract all instances of a pattern from a string, especially when the pattern includes groups to capture specific parts of the text. It's widely used in data parsing tasks like this one, where you need to extract structured information from unstructured text.
'''


# The cli method is used to execute CLI commands on the network device. 
# The entire output from the cli method is stored in the variable output. 
# output is a dictionary: key is 'show ip route' and value is 'all the output as a string'
output = device.cli(["show ip route"])   # dictionary['key']
print('output:', type(output))
print('output:', output)


# Retrieving and Printing the Raw Routing Table:
# output is assigned just the value, the string, of the the cli-output (no key of 'show ip route')
# Just the value (the actual output without the key 'show ip route' is assigned to _raw a string var
routing_table_raw = output["show ip route"]      # string_var = dictionary['key']

# print('routing_table_raw type', type(routing_table_raw))
print(routing_table_raw)  # Debug: Check the raw output



# Find all matches in the ios_output
# Process and print the results
# The code snippet below processes routing table data using regular expressions. 
# route_regex is a pre-compiled regular expression object that contains a pattern used to match routing table entries.
# .findall() is a method called on this regex object. It scans the string routing_table_raw for all non-overlapping occurrences of the pattern.
# routing_table_raw should be a string that contains the raw output of a routing table from a network device.
# The method returns a list of tuples (routes) where each tuple contains all the substrings found by the "capturing groups" in the regex pattern. Each tuple corresponds to one matched routing table entry.

routes = route_regex.findall(routing_table_raw)


# This is a loop that iterates over the list of tuples (routes) returned by .findall().
# Each route is a tuple with elements that correspond to the parts of the routing entry captured by the regex. 
# route is a list of tuples
# For example, protocol, network, etc.
# route: ('R', '192.168.3.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1')
# in routes [('S*', '0.0.0.0/0', '1', '0', '', '', 'via'), ('C', '192.168.2.0/24', '', '', '', 'directly connected,', 'GigabitEthernet0/1'), ('L', '192.168.2.1/32', '', '', '', 'directly connected,', 'GigabitEthernet0/1'), ('R', '192.168.3.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1'), ('R', '192.168.4.0/24', '120', '1', '192.168.2.2', '', 'GigabitEthernet0/1')]


# The tuple is unpacked into variables: protocol, network, distance, next_hop, description, interface. Each variable holds a part of the routing table entry that was matched by a corresponding named group in the regex pattern.
# Inside the loop, a formatted string is printed for each route. It uses f-strings (formatted string literals), which is a feature in Python that allows you to include expressions inside string literals, using curly braces {}.
# The f-string in the print statement will print out the protocol and network information for each route. The comma at the end of the print function call in your snippet seems to indicate that the original code may continue to print out additional information for each route.

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

# route_dictionary
# Now you can print the route information using the network as the key
# This dictionary will contain all prefixes but only one route per prefix (not ECMP)
# NAPALM get_route_to() is used to get all paths for each prefix

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

route_dictionary_final = {}
    
for network in route_dictionary.keys():
    print('for network in route_dictionary.keys():')
    pprint(device.get_route_to(network))
    
    
    
    route_info_final = {
        'protocol': protocol,
        'admin_distance': admin_distance if admin_distance else '0',
        'metric': metric if metric else 'N/A',
        'next_hop': next_hop if next_hop else 'N/A',
        'description': description.strip() if description else 'N/A',
        'interface': interface
    }

    # Use the network as the key for the main dictionary
    route_dictionary_final[network] = route_info

print('\n')
pprint('route_dictionary_final:')    
pprint(route_dictionary_final)