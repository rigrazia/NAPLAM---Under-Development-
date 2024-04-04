# List of dictionaries - each dictionary same keys, nothing to index the it on
# Because there is no unique key for each dictionary (like gig0/0 and gig0/1), 
# this data structure is a list of dictionaries

# Each dictionary represents a distinct record with several attributes that are logically related, like a row in a table or a record in a database.
# There isn't a single key that uniquely identifies each entry, or it's not practical to use one as the primary key for a dictionary. 
# For example, if 'interface' or 'ip' could have duplicates across records, they can't serve as unique keys.

# In a list of dictionaries:
# The order of the dictionaries is preserved, reflecting the sequence in which data was added or the order in which it should be processed.
# It allows for easy iteration over all records, with the ability to access each attribute by its key within each dictionary.
# It's flexible to add more dictionaries or remove some without worrying about maintaining unique keys.


device_arp = \
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


# print(device_arp)

print('\nEntry 0:')
print('\tage:', device_arp[0]['age'])
print('\tinterface:', device_arp[0]['interface'])
print('\tip:', device_arp[0]['ip'])
print('\tmac:', device_arp[0]['mac'])

print('\nEntry 1:')
print('\tage:', device_arp[1]['age'])
print('\tinterface:', device_arp[1]['interface'])
print('\tip:', device_arp[1]['ip'])
print('\tmac:', device_arp[1]['mac'])

print('\nEntry 2:')
print('\tage:', device_arp[2]['age'])
print('\tinterface:', device_arp[2]['interface'])
print('\tip:', device_arp[2]['ip'])
print('\tmac:', device_arp[2]['mac'])

# Do the same thing with a for loop
# entry is the variable name given to that iteration of the dictionary
#     ex: {'age': -1.0, 'interface': 'GigabitEthernet0/0', 'ip': '192.168.1.1', 'mac': 'B0:AA:77:09:3C:30'}
counter = 0
for entry in device_arp:
    # print(entry)
    print(f'\nEntry {counter}:')
    print('\tage:', entry['age'])
    print('\tinterface:', entry['interface'])
    print('\tip:', entry['ip'])
    print('\tmac:', entry['mac'])
    
    # counter = counter + 1
    counter += 1
