import json
from trafficanalyzer import *


# SAX Traffic 100 Gigabit Ethernet 4/1

incoming_traffic_ids = list()
incoming_traffic_ids.append('70338')

outgoing_traffic_ids = list()
outgoing_traffic_ids.append('70416')

all_traffic = TrafficAnalyzer()

print("Incoming")
for items_id in incoming_traffic_ids:
    results1 = all_traffic.get_traffic(items_id)

print("Outgoing")
for items_id in outgoing_traffic_ids:
    results2 = all_traffic.get_traffic(items_id)

final_result = list()
i = 0
while i < len(results1):
    tmp = list()
    tmp = results1[i]
    tmp = tmp + (results2[i][1],)
    final_result.append(tmp)
    i += 1

# Merged traffic as a json header
print("Merged Traffic")
dict_obj = {"SAX": {"name": "", "utc": True, "columns": ["time", "in, out"],
                     "points": final_result}}

r = json.dumps(dict_obj)
loaded_r = json.loads(r)
print(r)

'''
print()
for pair_values in my_dict:
    print("{0}: {1}".format(datetime.fromtimestamp(int(pair_values))
                            .strftime("%x %X"), my_dict[pair_values]))


print("All Traffic 2")
my_dict2 = dict()
my_dict2 = all_traffic.get_total_traffic2()

print()
for pair_values in my_dict2:
    print("{0}: {1}".format(datetime.fromtimestamp(int(pair_values))
                            .strftime("%x %X"), my_dict2[pair_values]))


# Conversion from dictionary to list
print()
dict_list = []
keys = list(my_dict.keys())
n = len(keys)
for i in range(0, n, 2):
    my_tuple = [keys[i], my_dict[keys[i]], my_dict[keys[i+1]]]
    dict_list.append(my_tuple)

# json header
dict_obj = {"SAX": {"name": "", "utc": True, "columns": ["time", "in, out"],
                     "points": dict_list}}

r = json.dumps(dict_obj)
loaded_r = json.loads(r)
print(r)
'''