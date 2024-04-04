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
    
    # Configuration lines
config_commands = [
    'interface GigabitEthernet0/1',  # Replace with the actual interface
    'ipv6 address 2001:DB8::1/64',   # Your Global Unicast Address (GUA)
    'ipv6 address FE80::1 link-local' # Your Link-Local Address (LLA)
]

# Load the configuration
device.load_merge_candidate(config=config_commands)

# Compare config and check the diff
print('Diff before commit:')
print(device.compare_config())

# Commit the configuration if all is good
try:
    choice = input("Commit these changes? [yN]: ")
    if choice.lower() == 'y':
        device.commit_config()
        print("Configuration committed successfully!")
    else:
        print("Configuration changes discarded.")
        device.discard_config()
except Exception as e:
    print(e)
    device.discard_config()

# Close the session
device.close()