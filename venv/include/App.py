import json
from trafficanalyzer import *


# SAX Traffic 100 Gigabit Ethernet 4/1

# incoming_traffic_ids.append('70339') # 4/2
# outgoing_traffic_ids.append('70417') # 4/2

all_traffic = TrafficAnalyzer('SAX', '70338', '70416')

# Merged traffic as a json object
traffic1 = list()
traffic1 = all_traffic.traffic_on_json()
# print()
# print()

# MCT01 Traffic 100 Gigabit Ethernet 7/2

# incoming_traffic_ids.append('59510') # 7/1
# outgoing_traffic_ids.append('59516') # 7/1

all_traffic = TrafficAnalyzer('MCT01', '59511', '59517')

# Merged traffic as a json object
traffic2 = all_traffic.traffic_on_json()

all_traffic.total_traffic(traffic1, traffic2)