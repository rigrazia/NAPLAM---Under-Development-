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

print('\n--------- Looping through dictionary: items method -----------------')
for key, value in device_facts.items():
    print(key, value)
    
print('\n--------- Looping through dictionary: keys method ------------------')
for key in device_facts.keys():
    print(key, device_facts[key])
    
print('\n--------- Looping through dictionary: no method ------------------')
for key in device_facts:
    print(key, device_facts[key])

print('\n--------- Looping through dictionary: values method ----------------')
for value in device_facts.values():
    print(value)



device.close()