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

# device.xxx() object is a DICTIONARY
print(type(device.get_environment()))

'''
By default, print() will output the dictionary as a single line without any special formatting. It will display the entire dictionary's content on one line.
'''

print('\n--------- Get Facts ---------')
# pprint(device.get_facts())
device_facts = device.get_facts()
pprint(device_facts)

print('\n--------- Get Environment ---------')
# pprint(device.get_environment())
device_environment = device.get_environment()
pprint(device_environment)

print('\n--------- Get Interfaces ---------')
# pprint(device.get_interfaces())
device_interfaces = device.get_interfaces()
pprint(device_interfaces)

print('\n--------- Get ARP Table ---------')
# pprint(device.get_arp_table())
device_arp_table = device.get_arp_table()
pprint(device_arp_table)

print('\n--------- Get Config ---------')
# print(device.get_config(retrieve='running', full=False))
device_config = device.get_config(retrieve='running', full=False)
pprint(device_config)




device.close()