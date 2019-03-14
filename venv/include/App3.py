import sys
import logging
from pyzabbix import ZabbixAPI
from datetime import datetime
from collections import OrderedDict
import time
import json

ZABBIX_SERVER = 'https://ultralog.ampath.net/zabbix'
ZABBIX_USER = 'apiuser'         # "apiuser"
ZABBIX_PSSW = 'Ciaraapiuser*'   # "Ciaraapiuser*"

zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login(ZABBIX_USER, ZABBIX_PSSW)

print("Connected to Zabbix API Version %s" % zapi.api_version())


# Get all items from an specific host
hostid = 10085
for i in zapi.item.get(output="extend",hostids=hostid,sortfield="itemid",sortorder='ASC'):
    print(i)

'''
# Get all monitored hosts
results = zapi.host.get(monitored_hosts=1, output='extend')

for result in results:
    print (result)
'''

# Get all items from an specific host
# hostid = 10165
# for i in zapi.item.get(output="extend",hostids=hostid,sortfield="type",sortorder='ASC'):
#    print(i)


# Miami (Brocade MCT01)
# hostid = 10085

# Incoming traffic on interface 100GigabitEthernet7/1
# From Miami (MCT02) to Miami (MCT01)
# itemid = 59510

# Incoming traffic on interface 100GigabitEthernet7/2                                          
# From Fortaleza Brazil (SAX) to Miami (MCT01)
# itemid = 59511


# Fortaleza Brazil (SAX)
# hostid = 10351

# Incoming traffic on interface 100GigabitEthernet4/1
# From Miami (MCT01) to Fortaleza Brazil (SAX)
# itemid = 70338

# Incoming traffic on interface 100GigabitEthernet4/2
# From Sao Paulo Brazil (vANSP-MLXe / SouthernLight2) to Fortaleza Brazil (SAX)
# itemid = 70339


# Sao Paulo Brazil (vANSP-MLXe / SouthernLight2)
# hostid = 10270

# Incoming traffic on interface 100GigabitEthernet6/1
# From Fortaleza Brazil (SAX) to Sao Paulo Brazil (vANSP-MLXe / SouthernLight2)
# itemid = 55764

# Incoming traffic on interface 100GigabitEthernet7/1
# From Chile (AndesLight) to Sao Paulo Brazil (vANSP-MLXe / SouthernLight2)
# itemid = 59650


# Chile (AndesLight)
# hostid = 10165

# Incoming traffic on interface 100GigabitEthernet3/1
# From Sao Paulo Brazil (vANSP-MLXe / SouthernLight2) to Chile (AndesLight)
# itemid = 65145

# Incoming traffic on interface 100GigabitEthernet3/2
# From Chile (AndesLight2) to Chile (AndesLight) 
# itemid = 65146


# Chile (AndesLight2)
# hostid = 10184

# Incoming traffic on interface 100GigabitEthernet3/2
# From Chile (AndesLight) to Chile (AndesLight2)
# itemid = 70648

# Incoming traffic on interface 100GigabitEthernet3/1
# From Panama (RedCLARA Panama) to Chile (AndesLight2)
# itemid = 70647



# ??????????????
# Panama (RedCLARA Panama)
# hostid = 10361

# Incoming traffic on interface HundredGigE0/1/0/1.872
# From Chile (AndesLight2) to Panama (RedCLARA Panama)
# itemid = 78771 (HundredGigE0/1/0/0)


# ??????????????


# San Juan PR (SJuan)
# hostid = 10359

# Incoming traffic on interface 100GigabitEthernet6/1
# From Panama (RedCLARA Panama) to San Juan PR (SJuan)
# itemid = 75481

# Incoming traffic on interface 100GigabitEthernet5/1
# From Miami (Brocade MCT02) to San Juan PR (SJuan)
# itemid = 75479


# Miami (Brocade MCT02)
# hostid = 10146

# Incoming traffic on interface 100GigabitEthernet7/2
# From San Juan PR (SJuan) to Miami (Brocade MCT02)
# itemid = 59533

# Incoming traffic on interface 100GigabitEthernet7/1
# From Miami (Brocade MCT01) to Miami (Brocade MCT02)
# itemid = 59532

'''
host_ids['SAX','10351'] = [['MCT01',[[1,'70338'],[-1,'59511']]], ['SouthernLight2', [[1,'70339'], [-1,'55764']]]]

host_ids['SouthernLight2','10270'] = [['SAX',[[1, '55764'], [-1,'70339']]], ['AndesLight', [[1, '59650'], [-1,'65145']]]]

host_ids['AndesLight','10165'] = [['SouthernLight2', [[1, '65145'], [-1, '59650']]], ['AndesLight2', [[1,'65146'], [-1,'70648']]]]

host_ids['AndesLight2','10184'] = [['AndesLight', [[1, '70648'], [-1, '65146']]], ['RedCLARA Panama', [[1, '70647'], [-1, '78771']]]]

host_ids['RedCLARA Panama','10361'] = [['AndesLight2', [[1, '78771'], [-1, '70647']]], ['San Juan', [[1, ''], [-1, '75481']]]]

host_ids['San Juan', '10359'] = [['RedCLARA Panama', [[1, '75481'], [-1, '']]], ['MCT02', [[1, '75479'], [-1, '59533']]]]

host_ids['MCT02', '10146'] = [['San Juan', [[1, '59533'], [-1, '75479']]], ['MTC01', [[1, '59532'], [-1, '59510']]]]

host_ids['MTC01', '10085'] = [['MTC02', [[1, '59510'], [-1, '59532']]], ['SAX', [[1, '59511'], [-1, '70338']]]]

'''
# incoming traffic in SAX
incoming_traffic_ids = []
# incoming_traffic_ids.append(('70338', '70339'))  # all incoming traffic to SAX

# incoming_traffic_ids.append(('55764', '59650'))  # all incoming traffic to SouthernLight2
# incoming_traffic_ids.append(('65145', '65146'))  # all incoming traffic to AndesLight
# incoming_traffic_ids.append(('70648', '70647'))  # all incoming traffic to AndesLight2
# incoming_traffic_ids.append(('78771'))           # all incoming traffic to RedCLARA Panama
# incoming_traffic_ids.append(('75481', '75479'))  # all incoming traffic to San Juan
# incoming_traffic_ids.append(('59533', '59532'))  # all incoming traffic to MCT02
# incoming_traffic_ids.append(('59510', '59511'))  # all incoming traffic to MCT01

# outgoing traffic from SAX
outgoing_traffic_ids = []
outgoing_traffic_ids.append(('59511', '55764'))  # all outgoing traffic from SAX

# outgoing_traffic_ids.append(('70339', '65145'))  # all outgoing traffic from SouthernLight2
# outgoing_traffic_ids.append(('59650', '70648'))  # all outgoing traffic from AndesLight
# outgoing_traffic_ids.append(('65146', '78771'))  # all outgoing traffic from AndesLight2
# outgoing_traffic_ids.append(('70647', '75481'))  # all outgoing traffic from RedCLARA Panama
# outgoing_traffic_ids.append(('59533'))           # all outgoing traffic from San Juan
# outgoing_traffic_ids.append(('75479', '59510'))  # all outgoing traffic from MCT02
# outgoing_traffic_ids.append(('59532', '70338'))  # all outgoing traffic from MCT01

time_till = time.mktime(datetime.now().timetuple())
time_from = time_till - 60 * 60  # last 1 hours

results = []


def gettraffic(source):
    result = []
    for item in source:
        # Query item's history (integer) data
        history = zapi.history.get(itemids=[item],
                                   time_from=time_from,
                                   time_till=time_till,
                                   output='extend',
                                   limit='5000'
                                   )

        # If nothing was found, try getting it from history (float) data
        if not len(history):
            history = zapi.history.get(itemids=[item],
                                       time_from=time_from,
                                       time_till=time_till,
                                       output='extend',
                                       limit='5000',
                                       history=0
                                       )

        # Print out each datapoint
        for point in history:
            result.append((int(point['clock']), point['value']))
            print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock']))
                                    .strftime("%x %X"), point['value']))

        result.sort()
        print()

    return result


def gettotaltraffic(source):
    mydict = {}
    for result in source:
        if mydict and result[0] in mydict.keys():
            mydict[result[0]] += int(result[1])
        else:
            mydict[result[0]] = int(result[1])
    return mydict


print("Incoming")
for items_id in incoming_traffic_ids:
    results1 = gettraffic(items_id)

print("Outgoing")
for items_id in outgoing_traffic_ids:
    results2 = gettraffic(items_id)

mydict1 = {}
mydict2 = {}

print("Incoming")
mydict1 = gettotaltraffic(results1)

print()
for myvalues in mydict1:
    print("{0}: {1}".format(datetime.fromtimestamp(int(myvalues))
                            .strftime("%x %X"), mydict1[myvalues]))

print()
print("Outgoing")
mydict2 = gettotaltraffic(results2)

print()
for myvalues in mydict2:
    print("{0}: {1}".format(datetime.fromtimestamp(int(myvalues))
                            .strftime("%x %X"), mydict2[myvalues]))



# Conversion from dictionary to list
print()
dictlist = []
for key, value in mydict1.items():
    temp = [key,value]
    dictlist.append(temp)
print(dictlist)

# json header
myDictObj = {"SAX":{"name": "", "utc": True, "columns": ["time", "in"], "points": dictlist}}

r = json.dumps(myDictObj)
loaded_r = json.loads(r)
print(r)

# mydict1 = sorted(mydict1.items())
incoming_traffic = []
incoming_traffic.append(("SAX",mydict1))
print(incoming_traffic)

# mydict2 = sorted(mydict2.items())
outgoing_traffic = []
outgoing_traffic.append(("SAX",mydict2))
print(outgoing_traffic)
