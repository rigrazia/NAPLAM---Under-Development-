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

routes = device.get_route_to(destination='192.168.4.0')
pprint(type(routes))  # Check the type of 'routes'
pprint(routes)        # Print the content of 'routes'

'''
print('\n--------- Get Route To ---------')
device_route_to = device.get_route_to(destination='192.168.4.0')
pprint(device_route_to)

print('\n--------- Get Config ---------')
device_config = device.get_config()
pprint(device_config)

print('\n--------- Get Interface IP ---------')
device_interfaces_ip = device.get_interfaces_ip()
pprint(device_interfaces_ip)
'''




device.close()