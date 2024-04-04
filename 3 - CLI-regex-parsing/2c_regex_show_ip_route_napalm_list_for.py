import napalm
import re
from pprint import pprint

# Define the driver for Cisco IOS
driver = napalm.get_network_driver('ios')

devices = ['192.168.1.1', '192.168.2.2']

for ip in devices:

    # Device details
    device = driver( hostname=ip, 
                    username='admin',
                    password='cisco',
                    optional_args={'secret':'class'} )


    # Open the connection to the device
    device.open()




    route_regex = re.compile(
        # Protocol with optional * for any route
        r'(?P<protocol>L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|U|o|P|\+|[*])\*?\s+'  
        r'(?P<prefix>\S+/\d+)\s+'  # Network (with CIDR notation)
        #r'(?:\[(?P<admin_distance>\d+)/(?P<metric>\d+)\]\s+)?'  # Separating Administrative distance and metric
        #r'(?:via\s+(?P<next_hop>\S+),\s+)?'  # Optional next-hop
        #r'(?:is\s+)?(?P<description>[\w\s-]+,)?\s*'  # Description (e.g., "directly connected")
        #r'(?:[0-9]{2}:[0-9]{2}:[0-9]{2},\s+)?'  # Optionally match the update time which is not needed
        #r'(?P<interface>\S+)'  # Interface
    )



    output = device.cli(["show ip route"])   # dictionary['key']
    #print('output:', type(output))
    #print('output:', output)


    routing_table_raw = output["show ip route"]      # string_var = dictionary['key']

    #print("Router IP:", ip)
    #print(routing_table_raw)  # Verify: Check the raw output

    '''Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
        D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
        N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
        E1 - OSPF external type 1, E2 - OSPF external type 2
        i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
        ia - IS-IS inter area, * - candidate default, U - per-user static route
        o - ODR, P - periodic downloaded static route, + - replicated route

    Gateway of last resort is 192.168.2.2 to network 0.0.0.0

    S*    0.0.0.0/0 [1/0] via 192.168.2.2
                    is directly connected, Loopback0
        10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
    C        10.0.0.0/24 is directly connected, Loopback0
    L        10.0.0.1/32 is directly connected, Loopback0
        192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks
    C        192.168.1.0/24 is directly connected, GigabitEthernet0/0
    L        192.168.1.1/32 is directly connected, GigabitEthernet0/0
        192.168.2.0/24 is variably subnetted, 2 subnets, 2 masks
    C        192.168.2.0/24 is directly connected, GigabitEthernet0/1
    L        192.168.2.1/32 is directly connected, GigabitEthernet0/1
        192.168.3.0/24 is variably subnetted, 2 subnets, 2 masks
    C        192.168.3.0/24 is directly connected, GigabitEthernet0/2
    L        192.168.3.1/32 is directly connected, GigabitEthernet0/2
    R     192.168.5.0/24 [120/1] via 192.168.3.2, 00:00:11, GigabitEthernet0/2
                        [120/1] via 192.168.2.2, 00:00:16, GigabitEthernet0/1'''


    routes = route_regex.findall(routing_table_raw)

    route_list_cliRegex = []

    # Process the results
    for route in routes:
        
        protocol, prefix = route
        #print("protocol, prefix", protocol, prefix)

        route_list_cliRegex.append(prefix)
        #print("prefix, route_list_cliRegex", prefix, route_list_cliRegex)

     

    #print("completed route_list_cliRegex")
    route_list_cliRegex = sorted(route_list_cliRegex)
    #print(route_list_cliRegex)



    for prefix in route_list_cliRegex:
        
        #print('route_dictionary_cliRegex:')
        #pprint(route_dictionary_cliRegex)
        #print()
        
        '''
        Prefix: 0.0.0.0/0

        Prefix: 10.0.0.0/24

        Prefix: 10.0.0.1/32

        Prefix: 192.168.1.0/24

        Prefix: 192.168.1.1/32

        Prefix: 192.168.2.0/24

        Prefix: 192.168.2.1/32

        Prefix: 192.168.3.0/24

        Prefix: 192.168.3.1/32

        Prefix: 192.168.5.0/24'''
        

    # Initialize an empty dictionary to hold all route information 
    # Prefixes from route_dictionary_cliRegex and routing information from NAPALM get_route_to()
    all_routes_cliRegex_napalmGRT = {}

        
    for prefix_cliRegex in route_list_cliRegex:
        
        # Get route information for the specific network
        route_info_napalmGRT = device.get_route_to(prefix_cliRegex)
        #print("route_info_napalmGRT", route_info_napalmGRT)
        
        # Store the route information in the all_routes_info dictionary
        all_routes_cliRegex_napalmGRT.update(route_info_napalmGRT)
        

    #print()
    #print("all_routes_cliRegex_napalmGRT:")
    #pprint(all_routes_cliRegex_napalmGRT)


    '''
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
    '10.0.0.0/24': [{'age': '',
                    'current_active': True,
                    'inactive_reason': '',
                    'last_active': True,
                    'next_hop': '',
                    'outgoing_interface': 'Loopback0',
                    'preference': 0,
                    'protocol': 'connected',
                    'protocol_attributes': {},
                    'routing_table': 'default',
                    'selected_next_hop': True}],
    '10.0.0.1/32': [{'age': '',
                    'current_active': True,
                    'inactive_reason': '',
                    'last_active': True,
                    'next_hop': '',
                    'outgoing_interface': 'Loopback0',
                    'preference': 0,
                    'protocol': 'connected',
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
    '192.168.1.1/32': [{'age': '',
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
    '192.168.2.1/32': [{'age': '',
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
    '192.168.3.0/24': [{'age': '',
                        'current_active': True,
                        'inactive_reason': '',
                        'last_active': True,
                        'next_hop': '',
                        'outgoing_interface': 'GigabitEthernet0/2',
                        'preference': 0,
                        'protocol': 'connected',
                        'protocol_attributes': {},
                        'routing_table': 'default',
                        'selected_next_hop': True}],
    '192.168.3.1/32': [{'age': '',
                        'current_active': True,
                        'inactive_reason': '',
                        'last_active': True,
                        'next_hop': '',
                        'outgoing_interface': 'GigabitEthernet0/2',
                        'preference': 0,
                        'protocol': 'connected',
                        'protocol_attributes': {},
                        'routing_table': 'default',
                        'selected_next_hop': True}],
    '192.168.5.0/24': [{'age': 0,
                        'current_active': True,
                        'inactive_reason': '',
                        'last_active': True,
                        'next_hop': '192.168.3.2',
                        'outgoing_interface': 'GigabitEthernet0/2',
                        'preference': 1,
                        'protocol': 'rip',
                        'protocol_attributes': {},
                        'routing_table': 'default',
                        'selected_next_hop': True},
                        {'age': 16,
                        'current_active': True,
                        'inactive_reason': '',
                        'last_active': True,
                        'next_hop': '192.168.2.2',
                        'outgoing_interface': 'GigabitEthernet0/1',
                        'preference': 1,
                        'protocol': 'rip',
                        'protocol_attributes': {},
                        'routing_table': 'default',
                        'selected_next_hop': True}]}
    '''


    ######### ACCESSING NESTED DICTIONARY


    '''
    print("dictionary: One of the keys in all_routes_info['192.168.5.0/24']")
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'])

    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['current_active'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['last_active'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['next_hop'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['outgoing_interface'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['preference'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['protocol'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['protocol_attributes'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['routing_table'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][0]['selected_next_hop'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['age'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['current_active'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['last_active'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['next_hop'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['outgoing_interface'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['preference'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['protocol'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['protocol_attributes'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['routing_table'])
    print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'][1]['selected_next_hop'])
    '''

    ######### END OF NEW CODE


    # all_routes_info is your nested dictionary

    # Iterate through each network in the dictionary

    #print()
    #print("IP Routing Table using all routes cli+GRT, dictionary: all_routes_cliRegex_napalmGRT")
    #print("------------------------------------------------------------------------------------")
    #print()
    
    print(f"Router IP: {ip}")

    for prefix_outer, routes_info_inner in all_routes_cliRegex_napalmGRT.items():
        # Now, routes_info_inner is the dictionary with route details list
        
        #print('ALL_ROUTES_INFO[NETWORK]:', all_routes_info[network])
        #print("dictionary: One of the keys, network (192.168.5.0/24) in all_routes_info.items()")
        #print("all_routes_info['192.168.5.0/24']")
        #print(all_routes_cliRegex_napalmGRT['192.168.5.0/24'])   
        
        #print("prefix_outer:", prefix_outer)
        
        '''
        {'192.168.5.0/24': [{'protocol': 'rip', 'outgoing_interface': 'GigabitEthernet0/2', 'age': 23, 'current_active': True, 'routing_table': 'default', 'last_active': True, 'protocol_attributes': {}, 'next_hop': '192.168.3.2', 'selected_next_hop': True, 'inactive_reason': '', 'preference': 1}, {'protocol': 'rip', 'outgoing_interface': 'GigabitEthernet0/1', 'age': 8, 'current_active': True, 'routing_table': 'default', 'last_active': True, 'protocol_attributes': {}, 'next_hop': '192.168.2.2', 'selected_next_hop': True, 'inactive_reason': '', 'preference': 1}]}
        '''
        
        
        # Iterate through each route detail dictionary in the list
        for route_detail_GRT in all_routes_cliRegex_napalmGRT[prefix_outer]:  # as each key corresponds to a list of dictionaries
            #print(f"ip: {ip}")
            #print(f"prefix_outer: {prefix_outer}")
            #print(f"route_detail_GRT: {route_detail_GRT}")

            print("\t", prefix_outer, route_detail_GRT['protocol'], route_detail_GRT['outgoing_interface'], route_detail_GRT['preference'])

            
            # Now print each key-value pair in the route detail
            #for key, value in route_detail_GRT.items():
                #print(f"  key: {key}: value: {value}")
                #print(f"  {key}: {value}")

                #print(route_detail_GRT['protocol'])
                
                #print(ip, prefix_outer, route_detail_GRT['protocol'], route_detail_GRT['outgoing_interface'])

            #print(f"    Specific detail - Outgoing Interface: {route_detail_GRT['outgoing_interface']}")        
            
            #print()  # Print a newline for better readability between each route detail               


            '''
            key 
            '192.168.5.0/24':
            [   
            value
                {'protocol': 'rip', 'outgoing_interface': 'GigabitEthernet0/2', 'age': 23, 'current_active': True,  'routing_table': 'default', 'last_active': True, 'protocol_attributes': {}, 'next_hop': '192.168.3.2', 'selected_next_hop': True, 'inactive_reason': '', 'preference': 1},
            
            key
            '192.168.5.0/24':
            value
                {'protocol': 'rip', 'outgoing_interface': 'GigabitEthernet0/1', 'age': 8, 'current_active': True, 'routing_table': 'default', 'last_active': True, 'protocol_attributes': {}, 'next_hop': '192.168.2.2', 'selected_next_hop': True, 'inactive_reason': '', 'preference': 1}
            ]
            '''

                

            
        '''
        IP Routing Table using all routes cli+GRT, dictionary: all_routes_cliRegex_napalmGRT
        ------------------------------------------------------------------------------------

        prefix_outer: 0.0.0.0/0
        protocol: static
        outgoing_interface: 
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 192.168.2.2
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 10.0.0.0/24
        protocol: connected
        outgoing_interface: Loopback0
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 10.0.0.1/32
        protocol: connected
        outgoing_interface: Loopback0
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.1.0/24
        protocol: connected
        outgoing_interface: GigabitEthernet0/0
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.1.1/32
        protocol: connected
        outgoing_interface: GigabitEthernet0/0
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.2.0/24
        protocol: connected
        outgoing_interface: GigabitEthernet0/1
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.2.1/32
        protocol: connected
        outgoing_interface: GigabitEthernet0/1
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.3.0/24
        protocol: connected
        outgoing_interface: GigabitEthernet0/2
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.3.1/32
        protocol: connected
        outgoing_interface: GigabitEthernet0/2
        age: 
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 
        selected_next_hop: True
        inactive_reason: 
        preference: 0

        prefix_outer: 192.168.5.0/24
        protocol: rip
        outgoing_interface: GigabitEthernet0/2
        age: 19
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 192.168.3.2
        selected_next_hop: True
        inactive_reason: 
        preference: 1

        prefix_outer: 192.168.5.0/24
        protocol: rip
        outgoing_interface: GigabitEthernet0/1
        age: 6
        current_active: True
        routing_table: default
        last_active: True
        protocol_attributes: {}
        next_hop: 192.168.2.2
        selected_next_hop: True
        inactive_reason: 
        preference: 1

        '''
