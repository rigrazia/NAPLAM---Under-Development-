'''For configurations router must be enabled for SCP: 
aaa new-model
aaa authentication login default local
aaa authorization exec default local 
username admin2 priv 15 password cisco # Need different username than ssh
ip scp server enable
'''

import napalm

devices = ['192.168.1.1']

ipv6_interface_list = [
    'ipv6 unicast-routing',
    
    'interface g0/0',
    'ipv6 address 2001:db8:cafe:1::1/64',
    'ipv6 address fe80::1:1 link-local',
    'exit',
    
    'interface g0/1',
    'ipv6 address 2001:db8:cafe:2::1/64',
    'ipv6 address fe80::1:2 link-local',
    'exit'
]

for device in devices:
    driver = napalm.get_network_driver('ios')
    device_object = driver(
        hostname=device,
        username='admin2',
        password='cisco',
        optional_args={'secret': 'class'}  # Replace with the actual enable password
    )

    device_object.open()
    #device_object.load_merge_candidate(config='\n'.join(ipv6_interface_list))
    device_object.load_merge_candidate(config='interface GigabitEthernet0/0\n ipv6 address 2001:db8:cafe:1::1/64\n end\n')

    # Compare the candidate configuration with the running configuration
    diff = device_object.compare_config()

    # If there are changes, commit the configuration
    if diff:
        print(f"Applying configuration on {device}:")
        print(diff)

        # Commit the changes (This will replace the running configuration with the candidate configuration)
        device_object.commit_config()

        # Discard the changes in the candidate configuration
        device_object.discard_config()
    else:
        print(f"No configuration changes needed for {device}")

    print(device)
    print('-' * 11)
    print(device_object.get_interfaces_ip())

    print('\n')

    device_object.close()
