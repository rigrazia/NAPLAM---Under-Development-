# Dictionary with a nested list
from pprint import pprint

device_facts = {
  "uptime": 240.0,
  "vendor": "Cisco",
  "os_version": "C2900 Software (C2900-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)",
  "serial_number": "FCZ150425YC",
  "model": "CISCO2911/K9",
  "hostname": "R1",
  "fqdn": "R1.ssh-key.com",
  "interface_list": [
    "GigabitEthernet0/0",
    "GigabitEthernet0/1",
    "GigabitEthernet0/2"
  ]
}


# pprint(device_facts)
print("\n")
print("Model:", device_facts['model'])  
print("OS Version:", device_facts['os_version']) 
print("Vendor:", device_facts['vendor'])
print("Serial Number:", device_facts['serial_number'])  
print("FQDN:", device_facts['fqdn'])  
print("Uptime:", device_facts['uptime']) 
print("Interface List:", device_facts['interface_list']) 

# print key interface_list, print all the values within the list
# "interface_list": [ "GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2" ]
print("\nInterfaces:")
for interface in device_facts['interface_list']:
    print("\tInterface:", interface) 

# Using enumerate function, which provides the index along with the item during iteration 
print("\nInterfaces:")
for index, interface in enumerate(device_facts['interface_list']):
    print("\tIndex - Interface:", index, interface) 

# Accessing both key and value with method
for device in device_facts:  
  print(device, device_facts[device])
