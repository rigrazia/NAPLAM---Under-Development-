import re

def show_ip_route(device):
    route_regex = re.compile(r'^(?P<protocol>[A-KM-Z]\*?)\s+(?P<destination>\S+)')
    output = device.cli(["show ip route"])
    routing_table_raw = output["show ip route"]
    
    # Change destinations to a dictionary with destinations as keys and lists of routes as values
    destinations = {}

    for line in routing_table_raw.splitlines():
        match = route_regex.search(line)
        if match:
            protocol = match.group('protocol')
            destination = match.group('destination')
            
            # If destination is already in the dictionary, append the new route to its list
            if destination in destinations:
                destinations[destination].append(protocol)
            else:
                # Otherwise, create a new entry with this destination as the key
                destinations[destination] = [protocol]

    detailed_routing_table = {}

    for destination, protocols in destinations.items():
        # For each destination, we may now have multiple protocols/routes
        detailed_routes = []
        for protocol in protocols:
            # Retrieve and store detailed routing information for each protocol/route
            route_details = device.get_route_to(destination=destination)
            detailed_routes.append(route_details[destination])  # Assuming route_details is structured this way

        detailed_routing_table[destination] = detailed_routes  # Store the list of detailed routes

    print('\nDetailed Routing Table:', detailed_routing_table)
    return detailed_routing_table

# Device interaction would be done outside of this function
# device = <device_connection_object>
# show_ip_route(device)
