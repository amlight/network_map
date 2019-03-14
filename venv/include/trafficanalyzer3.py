from pyzabbix import ZabbixAPI
import time
import json
from datetime import datetime


class TrafficAnalyzer:

    def __init__(self, in_traffic_tag, in_incoming_traffic_id, in_outgoing_traffic_id):
        
        self.traffic_tag = in_traffic_tag
        self.incoming_traffic_id = in_incoming_traffic_id
        self.outgoing_traffic_id = in_outgoing_traffic_id
        
        self.final_result = list()
        
        """
        Zabbix API Credentials
        """
        self.ZABBIX_SERVER = 'https://ultralog.ampath.net/zabbix'
        self.ZABBIX_USER = 'apiuser'        # "apiuser"
        self.ZABBIX_PSSW = 'Ciaraapiuser*'  # "Ciaraapiuser*"

        self.zapi = ZabbixAPI(self.ZABBIX_SERVER)
        self.zapi.login(self.ZABBIX_USER, self.ZABBIX_PSSW)

        """
        Time frame to be considered
        """
        self.time_till = time.mktime(datetime.now().timetuple())
        self.time_from = self.time_till - 60 * 60 * 1  # last 1 hours

        # print("Connected to Zabbix API Version %s" % self.zapi.api_version())

    """
        Method to retrieve the historical values from some item (port) given its ID
        API connection to get item's history 
        The returned values contains the item id, clock, value, and ns
    """
    def check_traffic(self, source):
        result = list()
        # Query item's history (integer) data

        history = self.zapi.history.get(itemids=[source],
                                        time_from=self.time_from,
                                        time_till=self.time_till,
                                        output='extend',
                                        limit='5000')

        # If nothing was found, try getting it from history (float) data
        if not len(history):
            history = self.zapi.history.get(itemids=[source],
                                            time_from=self.time_from,
                                            time_till=self.time_till,
                                            output='extend',
                                            limit='5000',
                                            history=0)

        # Create the list with entries using each data point information
        for point in history:
            result.append((int(point['clock']), int(point['value'])))
            # print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock']))
            #                         .strftime("%x %X"), point['value']))

        # print()
        return result

    """
        Method to check Node/Port traffic
    """
    def get_traffic(self, traffic_type='in'):
        if traffic_type == 'in':
            return self.check_traffic(self.incoming_traffic_id)
        else:
            return self.check_traffic(self.outgoing_traffic_id)

    """
        Method to merge both traffic values in a same Data Structure
    """
    def merge_traffic(self, source1, source2):
        i = 0
        while i < len(source1):
            tmp = list()
            tmp = source1[i]
            tmp = tmp + (source2[i][1],)
            self.final_result.append(tmp)
            i += 1
    
    def build_json(self):

        # print("Incoming")
        results1 = self.get_traffic('in')

        # print("Outgoing")
        results2 = self.get_traffic('out')

        self.merge_traffic(results1, results2)
        
        print("Merged Traffic")
        dict_obj = {self.traffic_tag: {"name": "", "utc": True, "columns": ["time", "in, out"],
                                       "points": self.final_result}}
        r = json.dumps(dict_obj)
        loaded_r = json.loads(r)
        print(r)
        
        return self.final_result
    
    def total_traffic(self, source1, source2):
        i = 0
        out_total_traffic = list()
        while i < len(source1):
            tmp = (source1[i][0], source1[i][1] + source2[i][1], source1[i][2] + source2[i][2])
            out_total_traffic.append(tmp)
            i += 1

        print("Total Traffic")
        dict_obj = {"Total": {"name": "", "utc": True, "columns": ["time", "in, out"],
                                       "points": out_total_traffic}}
        r = json.dumps(dict_obj)
        loaded_r = json.loads(r)
        print(r)

