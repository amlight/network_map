import json
from trafficanalyzer import *


# SAX Traffic 100 Gigabit Ethernet 4/1
# incoming_traffic_ids.append('70339') # 4/2
# outgoing_traffic_ids.append('70417') # 4/2

# incoming_traffic_ids = list()
# incoming_traffic_ids.append('70338')

# outgoing_traffic_ids = list()
# outgoing_traffic_ids.append('70416')

all_traffic = TrafficAnalyzer('SAX', '70338', '70416')

print("Incoming")
# for items_id in incoming_traffic_ids:
#    results1 = all_traffic.get_traffic(all_traffic.)
results1= all_traffic.get_incoming_traffic()

print("Outgoing")
# for items_id in outgoing_traffic_ids:
#    results2 = all_traffic.get_traffic(items_id)
results2 = all_traffic.get_outgoing_traffic()

final_result = list()
final_result = all_traffic.merge_traffic(results1, results2)

# Merged traffic as a json object
all_traffic.build_json(final_result)
print()
print()

# MCT01 Traffic 100 Gigabit Ethernet 7/2

incoming_traffic_ids.clear()
incoming_traffic_ids.append('59511')
# incoming_traffic_ids.append('59510') # 7/1

outgoing_traffic_ids.clear()
outgoing_traffic_ids.append('59517')
# incoming_traffic_ids.append('59516') # 7/1

print("Incoming")
for items_id in incoming_traffic_ids:
    results1 = all_traffic.get_traffic(items_id)

print("Outgoing")
for items_id in outgoing_traffic_ids:
    results2 = all_traffic.get_traffic(items_id)

final_result.clear()
final_result = all_traffic.merge_traffic(results1, results2)

# Merged traffic as a json object
all_traffic.build_json(final_result)


