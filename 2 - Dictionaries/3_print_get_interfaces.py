# Nested dictionaries but with same values so we can use for loop with keys method
# Each key (interface key) is unique 

device_interfaces =   \
{'Embedded-Service-Engine0/0': {'description': '',
                                'is_enabled': False,
                                'is_up': False,
                                'last_flapped': -1.0,
                                'mac_address': '00:00:00:00:00:00',
                                'mtu': 1500,
                                'speed': 10.0},

 'GigabitEthernet0/0': {'description': '',
                        'is_enabled': True,
                        'is_up': True,
                        'last_flapped': -1.0,
                        'mac_address': 'B0:AA:77:09:3C:30',
                        'mtu': 1500,
                        'speed': 1000.0},
 'GigabitEthernet0/1': {'description': '',
                        'is_enabled': True,
                        'is_up': False,
                        'last_flapped': -1.0,
                        'mac_address': 'B0:AA:77:09:3C:31',
                        'mtu': 1500,
                        'speed': 1000.0},
'Serial0/0/0': {'description': '',
                 'is_enabled': False,
                 'is_up': False,
                 'last_flapped': -1.0,
                 'mac_address': '',
                 'mtu': 1500,
                 'speed': 1.544}, 'Serial0/0/1': {'description': '',
                 'is_enabled': False,
                 'is_up': False,
                 'last_flapped': -1.0,
                 'mac_address': '',
                 'mtu': 1500,
                 'speed': 1.544},
'Serial0/0/1': {'description': '',
                 'is_enabled': False,
                 'is_up': False,
                 'last_flapped': -1.0,
                 'mac_address': '',
                 'mtu': 1500,
                 'speed': 1.544}
}

# print(device_interfaces)

print("Interface:", device_interfaces['Embedded-Service-Engine0/0'])
print("Interface:", device_interfaces['GigabitEthernet0/0'])
# Interface: {'description': '', 'is_enabled': True, 'is_up': True, 'last_flapped': -1.0, 'mac_address': 'B0:AA:77:09:3C:30', 'mtu': 1500, 'speed': 1000.0}
print("Interface:", device_interfaces['GigabitEthernet0/1'])
print("Interface:", device_interfaces['Serial0/0/0'])
print("Interface:", device_interfaces['Serial0/0/1'])
# Interface: {'description': '', 'is_enabled': False, 'is_up': False, 'last_flapped': -1.0, 'mac_address': '', 'mtu': 1500, 'speed': 1.544}

# Loop through key (interface) and display same dictionary keys and their values for each interfaces
for interface in device_interfaces.keys():
    print("\n",interface)    # prints the key
    print("\tdescription:", device_interfaces[interface]['description'])
    print("\tis enabled:", device_interfaces[interface]['is_enabled'])
    print("\tis up:", device_interfaces[interface]['is_up'])
    print("\tlast flapped:", device_interfaces[interface]['last_flapped'])
    print("\tmac address:", device_interfaces[interface]['mac_address'])
    print("\tmtu:", device_interfaces[interface]['mtu'])
    print("\tspeed:", device_interfaces[interface]['speed'])
    
# Alternative loop through items to display same dictionary keys and their values for each interfaces
for interface, value in device_interfaces.items():
    print("\n",interface)    # prints the key > GigabitEthernet0/0
    print("\n",value)    # prints the value
    # value > {'description': '', 'is_enabled': True, 'is_up': True, 'last_flapped': -1.0, 'mac_address': 'B0:AA:77:09:3C:30', 'mtu': 1500, 'speed': 1000.0}
    print("\tdescription:", value['description'])
    print("\tis enabled:", value['is_enabled'])
    print("\tis up:", value['is_up'])
    print("\tlast flapped:", value['last_flapped'])
    print("\tmac address:", value['mac_address'])
    print("\tmtu:", value['mtu'])
    print("\tspeed:", value['speed'])