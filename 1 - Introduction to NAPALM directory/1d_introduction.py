import napalm 
from pprint import pprint

driver = napalm.get_network_driver('ios')
 
device = driver(
                hostname='192.168.1.1', 
                username='admin',
                password='cisco',
                optional_args={'secret':'class'}
            )

device.open()


print('\n--------- Get Facts ---------')
device_facts = device.get_facts()
pprint(device_facts)

print("\nGet Facts: device_facts['model']")
print("Model:", device_facts['model'])  

print("\nGet Facts: device_facts['os_version']")
print("OS Version:", device_facts['os_version']) 

print("\nGet Facts: device_facts['vendor']")
print("Vendor:", device_facts['vendor'])

print("\nGet Facts: device_facts['serial_number']")
print("Serial Number:", device_facts['serial_number'])  

print("\nGet Facts: device_facts['fqdn']")
print("FQDN:", device_facts['fqdn'])  

print("\nGet Facts: device_facts['uptime']")
print("Uptime:", device_facts['uptime']) 

print("\nGet Facts: device_facts['interface_list']")
print("Interface List:", device_facts['interface_list']) 

device.close()