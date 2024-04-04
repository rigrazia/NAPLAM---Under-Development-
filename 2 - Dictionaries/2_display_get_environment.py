# Nested Dictionaries
# Single main dicionary with nested dictionaries

from pprint import pprint

device_environment = {'cpu': {0: {'%usage': 3.0}},
 'fans': {'invalid': {'status': True}},
 'memory': {'available_ram': 338024304, 'used_ram': 87474120},
 'power': {'invalid': {'capacity': -1.0, 'output': -1.0, 'status': True}},
 'temperature': {'invalid': {'is_alert': False,
                             'is_critical': False,
                             'temperature': -1.0}}}



# pprint(device_facts)
print("\n")
print("cpu:", device_environment['cpu'])                             # {0: {'%usage': 3.0}}
print("\cpu-0:", device_environment['cpu'][0])                      #     {'%usage': 3.0}
print("\t\cpu-0-%usage:", device_environment['cpu'][0]['%usage'])   #                3.0

print("\n")
print("fans:", device_environment['fans'])                                   # {'invalid': {'status': True}}
print("\tfans-invalid:", device_environment['fans']['invalid'])              #             {'status': True}
print("\t\tfans-invalid-status:", device_environment['fans']['invalid']['status'])      #             True

print("\n")
print("memory:", device_environment['memory'])                  # {'available_ram': 338024304, 'used_ram': 87474120}
print("\tmemory-available_ram:", device_environment['memory']['available_ram'])   # 338024304
print("\tmemory-used_ram:", device_environment['memory']['used_ram'])             #                        87474120

print("\n")
print("power:", device_environment['power'])           # {'invalid': {'capacity': -1.0, 'output': -1.0, 'status': True}}
print("\tpower-invalid:", device_environment['power']['invalid']) #  {'capacity': -1.0, 'output': -1.0, 'status': True}
print("\t\tpower-invalid-capacity:", device_environment['power']['invalid']['capacity'])  # <-1.0
print("\t\tpower-invalid-output:", device_environment['power']['invalid']['output'])      #       -1.0
print("\t\tpower-invalid-status:", device_environment['power']['invalid']['status'])      #                       True

print("temperature:", device_environment['temperature'])  
                                           # {'invalid': {'is_alert': False, 'is_critical': False, 'temperature': -1.0}}
print("\ttemperature-invalid:", device_environment['temperature']['invalid']) 
                                           #             {'is_alert': False, 'is_critical': False, 'temperature': -1.0}
print("\t\ttemperature-invalid-is_alert:", device_environment['temperature']['invalid']['is_alert'])     # <False
print("\t\ttemperature-invalid-is_critical:", device_environment['temperature']['invalid']['is_critical'])  #   <False
print("\t\ttemperature-invalid-temperature:", device_environment['temperature']['invalid']['temperature'])  #     -1.0