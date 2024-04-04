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
# With pprint()
# Can also use: pprint(device.get_facts())
device_facts = device.get_facts()
print("\nDisplayed with pprint() - Alphabetical by key")
pprint(device_facts)

'''
# With json.dumps() - json.dumps() - dump string - is used to serialize the device_facts dictionary into a JSON-like formatted string. Displayed as a string formatted with indentation or assigned to string variable formatted_json_string and variable printed. 
print("\nDisplayed with json.dumps() - Order preset")
# print(json.dumps(device_facts, indent=2))
formatted_json_string = json.dumps(device_facts, indent=2)
print(formatted_json_string)
'''

device.close()