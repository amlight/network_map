import sys
import logging
from pyzabbix import ZabbixAPI
from datetime import datetime
import time

ZABBIX_SERVER = 'https://ultralog.ampath.net/zabbix'
ZABBIX_USER = 'apiuser'         # "apiuser"
ZABBIX_PSSW = 'Ciaraapiuser*'   # "Ciaraapiuser*"

zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login(ZABBIX_USER, ZABBIX_PSSW)

print("Connected to Zabbix API Version %s" % zapi.api_version())

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
incoming_traffic_ids.append(('70338', '70339'))  # all incoming traffic to SAX from MCT01

outgoing_traffic_ids = []
outgoing_traffic_ids.append(('59511', '55764'))  # all outgoing traffic from SAX to MCT01


time_till = time.mktime(datetime.now().timetuple())
time_from = time_till - 60 * 60  # last 1 hours

results = []

for items_id in incoming_traffic_ids:
    for item in items_id:
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
            results.append((int(point['clock']), point['value']))
            print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock']))
                                     .strftime("%x %X"), point['value']))
        print()
        print("Next")
        print()
        results.sort()

mydict = {}
for result in results:
    if mydict and result[0] in mydict.keys():
        mydict[result[0]] += int(result[1])
    else:
        mydict[result[0]] = int (result[1])

print()
for myvalues in mydict:
    print("{0}: {1}".format(datetime.fromtimestamp(int(myvalues))
                            .strftime("%x %X"), mydict[myvalues]))

incoming_traffic = []
incoming_traffic.append(("SAX",mydict))
print(incoming_traffic)
