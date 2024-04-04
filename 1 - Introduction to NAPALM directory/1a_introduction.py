# Imports the NAPALM library, for interacting with different network devices 
import napalm 

# Function that selects network driver,'ios', and returns driver object
# Can have different network drivers (ios_driver), and assign them to different device objects (ios_device).
driver = napalm.get_network_driver('ios')

# Creates a device object using the previously selected driver. 
# Provides connection details. 
device = driver(
                hostname='192.168.1.1', 
                username='admin',
                password='cisco',
                optional_args={'secret':'class'}
            )

# Establishes a connection to the specified network device using the connection details provided. 
device.open()

# device.xxx() object is a DICTIONARY
# print(type(device.get_facts()))

'''
By default, print() will output the dictionary as a single line without any special formatting. It will display the entire dictionary's content on one line.

Use pprint
'''

# get_facts() method retrieves information about the device, such as its hostname, model, serial number, etc. 
# device.xxx() object is a DICTIONARY
# Calling the get_facts() method on the device object and printing the result to the console.
print('\n--- Get Facts - get_facts() object ----')
print(device.get_facts())
# print("\ndevice.get_facts() is of type: ",type(device.get_facts()))

print('\n--- Get Facts - device_facts variable ----')
device_facts = device.get_facts()
# device_facts variable is of type dictionary 
# print("\ndevice_facts is a ", type(device_facts))
print(device_facts)


#print("\n")

# Closes the connection to the network device (good practice)
device.close()