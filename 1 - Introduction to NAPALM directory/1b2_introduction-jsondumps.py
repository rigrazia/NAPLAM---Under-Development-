import napalm 
from pprint import pprint
import json

driver = napalm.get_network_driver('ios')
 
device = driver(
                hostname='192.168.1.1', 
                username='admin',
                password='cisco',
                optional_args={'secret':'class'}
            )

device.open()


print('\n--------- Get Facts ---------')
pprint(device.get_facts())

# With pprint()
device_facts = device.get_facts()
print("\nDisplayed with pprint() - Alphabetical by key")
pprint(device_facts)

# With json.dumps() - json.dumps() is used to serialize the device_facts dictionary into a JSON-like formatted string. 
print("\nDisplayed with json.dumps() - Order preset")
print(json.dumps(device_facts, indent=2))

device.close()