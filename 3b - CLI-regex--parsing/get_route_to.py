import napalm
import re

# Replace with your device details
ip_address = "192.168.1.1"  # IP address of your Cisco device
username = "admin"          # your username
password = "cisco"          # your password

# Setup a driver for IOS
driver = napalm.get_network_driver("ios")

# Connect to the device
device = driver(hostname=ip_address, username=username, password=password)
device.open()

# Use the cli method to get the routing table
routing_table_raw = device.cli(["show ip route"])

# Regex to match network addresses (e.g., 192.168.1.0/24)
# This pattern might need adjustments based on actual output and variations in routing table format
network_regex = r"(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}\b)"

# Find all network addresses in the routing table
# Ensure to target the correct part of the routing_table_raw output
routing_table = routing_table_raw["show ip route"]
dest_networks = re.findall(network_regex, routing_table)

# Removing duplicates, as there might be multiple entries/routes for the same network
dest_networks = list(set(dest_networks))

# Iterate over each network and get route details
for network in dest_networks:
    try:
        route_details = device.get_route_to(destination=network)
        print(f"Routes to {network}:")
        for details in route_details:
            print(details)
        if len(route_details) > 1:
            print(f"Multiple paths found for {network}")
    except Exception as e:
        print(f"Could not retrieve route for {network}: {e}")

# Close the connection
device.close()
