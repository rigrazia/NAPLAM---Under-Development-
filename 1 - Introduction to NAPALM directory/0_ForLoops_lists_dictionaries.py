dictionary_device_facts = \
{
 'fqdn': 'R1.ssh-key.com',
 'hostname': 'R1',
 'interface_list': ['GigabitEthernet0/0',
                    'GigabitEthernet0/1',
                    'GigabitEthernet0/2'],
 'model': 'CISCO2911/K9',
 'os_version': 'C2900 Software (C2900-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)',
 'serial_number': 'FCZ150425YC',
 'uptime': 4740.0,
 'vendor': 'Cisco'
}


dictionary_mac_table = \
[
 {'age': -1.0,
  'interface': 'GigabitEthernet0/0',
  'ip': '192.168.1.1',
  'mac': 'B0:AA:77:09:3C:30'},
 {'age': 0.0,
  'interface': 'GigabitEthernet0/0',
  'ip': '192.168.1.100',
  'mac': '00:E0:4C:42:8D:D5'},
 {'age': -1.0,
  'interface': 'GigabitEthernet0/1',
  'ip': '192.168.2.1',
  'mac': 'B0:AA:77:09:3C:31'}
]



dictionary_a = {
                'age': 19,
                'current_active': True,
                'inactive_reason': '',
                'last_active': True,
                'next_hop': '192.168.3.2',
                'outgoing_interface': 'GigabitEthernet0/2',
                'preference': 1,
                'protocol': 'rip',
                'protocol_attributes': {},
                'routing_table': 'default',
                'selected_next_hop': True
                }


dictionary_b = {
                '0.0.0.0/0': {
                                'admin_distance': '1',
                                'description': 'N/A',
                                'interface': '',
                                'metric': '0',
                                'next_hop': 'N/A',
                                'protocol': 'S'
                            },
                '10.0.0.0/24': {'admin_distance': '0',
                                'description': 'directly connected,',
                                'interface': 'Loopback0',
                                'metric': 'N/A',
                                'next_hop': 'N/A',
                                'protocol': 'C'},
                '10.0.0.1/32': {'admin_distance': '0',
                                'description': 'Local interface',
                                'interface': 'Loopback0',
                                'metric': 'N/A',
                                'next_hop': 'N/A',
                                'protocol': 'L'},
                '192.168.1.0/24': {'admin_distance': '0',
                                    'description': 'directly connected,',
                                    'interface': 'GigabitEthernet0/0',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'C'},
                '192.168.1.1/32': {'admin_distance': '0',
                                    'description': 'Local interface',
                                    'interface': 'GigabitEthernet0/0',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'L'},
                '192.168.2.0/24': {'admin_distance': '0',
                                    'description': 'directly connected,',
                                    'interface': 'GigabitEthernet0/1',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'C'},
                '192.168.2.1/32': {'admin_distance': '0',
                                    'description': 'Local interface',
                                    'interface': 'GigabitEthernet0/1',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'L'},
                '192.168.3.0/24': {'admin_distance': '0',
                                    'description': 'directly connected,',
                                    'interface': 'GigabitEthernet0/2',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'C'},
                '192.168.3.1/32': {'admin_distance': '0',
                                    'description': 'Local interface',
                                    'interface': 'GigabitEthernet0/2',
                                    'metric': 'N/A',
                                    'next_hop': 'N/A',
                                    'protocol': 'L'},
                '192.168.5.0/24': {'admin_distance': '120',
                                    'description': 'N/A',
                                    'interface': 'GigabitEthernet0/2',
                                    'metric': '1',
                                    'next_hop': '192.168.3.2',
                                    'protocol': 'R'}    
                }

'''dictionary_c = \
{
  {'0.0.0.0/0': [
                    { 
                    'age': '',
                    'current_active': True,
                    'inactive_reason': '',
                    'last_active': True,
                    'next_hop': '192.168.2.2',
                    'outgoing_interface': '',
                    'preference': 0,
                    'protocol': 'static',
                    'protocol_attributes': {},
                    'routing_table': 'default',
                    'selected_next_hop': True}
                 ]
  },
{'10.0.0.0/24': [{'age': '',
                                  'current_active': True,
                                  'inactive_reason': '',
                                  'last_active': True,
                                  'next_hop': '',
                                  'outgoing_interface': 'Loopback0',
                                  'preference': 0,
                                  'protocol': 'connected',
                                  'protocol_attributes': {},
                                  'routing_table': 'default',
                                  'selected_next_hop': True}]},
{'10.0.0.1/32': [{'age': '',
                                  'current_active': True,
                                  'inactive_reason': '',
                                  'last_active': True,
                                  'next_hop': '',
                                  'outgoing_interface': 'Loopback0',
                                  'preference': 0,
                                  'protocol': 'connected',
                                  'protocol_attributes': {},
                                  'routing_table': 'default',
                                  'selected_next_hop': True}]},
 {'192.168.1.0/24': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/0',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
 {'192.168.1.1/32': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/0',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
 {'192.168.2.0/24': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/1',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
{'192.168.2.1/32': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/1',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
 {'192.168.3.0/24': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/2',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
 {'192.168.3.1/32': [{'age': '',
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '',
                                        'outgoing_interface': 'GigabitEthernet0/2',
                                        'preference': 0,
                                        'protocol': 'connected',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]},
 {'192.168.5.0/24': [{'age': 19,
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '192.168.3.2',
                                        'outgoing_interface': 'GigabitEthernet0/2',
                                        'preference': 1,
                                        'protocol': 'rip',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True},
                                       {'age': 6,
                                        'current_active': True,
                                        'inactive_reason': '',
                                        'last_active': True,
                                        'next_hop': '192.168.2.2',
                                        'outgoing_interface': 'GigabitEthernet0/1',
                                        'preference': 1,
                                        'protocol': 'rip',
                                        'protocol_attributes': {},
                                        'routing_table': 'default',
                                        'selected_next_hop': True}]}
 }'''



for key in dictionary_a:
    print(key, dictionary_a[key])
    
for key, value in dictionary_device_facts.items():

    # To iterface over list within a dictionary
    if isinstance(value, list):
        print(key)
        for item_list in value:
            print("\t", item_list)
    else:
        print(key, dictionary_device_facts[key])