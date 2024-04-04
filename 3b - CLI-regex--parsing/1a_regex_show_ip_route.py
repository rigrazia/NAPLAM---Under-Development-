import re
from pprint import pprint

# ios_output is as previously defined
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
R     192.168.4.0/24 [120/1] via 192.168.2.2, 00:00:17, GigabitEthernet0/1'''

# Regular expression to match routing table entries
# Assuming routing table entries are structured as:
# Code Network/Mask [Admin/Metric] via Next-Hop, Time, Interface
# Explanation:
# \w matches any single word character (equivalent to [a-zA-Z0-9_]).
# \S+ matches a sequence of non-whitespace characters.
# \d+ matches one or more digits.
# [...] is used to capture a group of characters as a match.
# (?:...)? is a non-capturing group that makes the 'via Next-Hop' part optional, because not all entries might have a next-hop defined (like connected routes).

# Define a regex pattern to match the routing table entries
# Considerations:
# - Protocols might be represented by a single letter followed by an optional asterisk
# - Network with prefix length
# - Optional [Administrative distance/metric]
# - Optional next-hop information prefixed by "via"
# - Optional age and exit interface information

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

# Find all matches in the ios_output
routes = route_regex.findall(ios_output)

route_dictionary = {}

# Process the results
for route in routes:
    # Next line tuple unpacking. This is a convenient way to assign each element of the route tuple to a separate variable.
    protocol, network, admin_distance, metric, next_hop, description, interface = route
    print('route:', route)
    print('in routes', routes)
    
    # Create a nested dictionary for each route
    route_info = {
        'protocol': protocol,
        'admin_distance': admin_distance if admin_distance else 'N/A',
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
    print('route_dictonary:')
    pprint(route_dictionary)
    print()