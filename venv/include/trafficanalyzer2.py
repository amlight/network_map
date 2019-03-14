from pyzabbix import ZabbixAPI
import time
import json
from datetime import datetime


class TrafficAnalyzer:

    def __init__(self, in_traffic_tag, in_incoming_traffic_id, in_outgoing_traffic_id):
        self.my_dict = dict()
        
        self.traffic_tag = in_traffic_tag
        self.incoming_traffic_id = in_incoming_traffic_id
        self.outgoing_traffic_id = in_outgoing_traffic_id
        
        """
        Zabbix API Credentials
        """
        self.ZABBIX_SERVER = 'https://ultralog.ampath.net/zabbix'
        self.ZABBIX_USER = 'apiuser'        # "apiuser"
        self.ZABBIX_PSSW = 'Ciaraapiuser*'  # "Ciaraapiuser*"

        self.zapi = ZabbixAPI(self.ZABBIX_SERVER)
        self.zapi.login(self.ZABBIX_USER, self.ZABBIX_PSSW)

        '''
            Time frame to be considered
        '''
        self.time_till = time.mktime(datetime.now().timetuple())
        self.time_from = self.time_till - 60 * 60 * 1  # last 1 hours

        print("Connected to Zabbix API Version %s" % self.zapi.api_version())

    """
        Method to get the historical values from some item (port) given its ID
        The returned values contains the item id, clock, value, and ns
    """
    def get_traffic(self, source):
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
            print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock']))
                                    .strftime("%x %X"), point['value']))

        print()
        return result
    
    def get_incoming_traffic(self):
        return self.get_traffic(self.incoming_traffic_id)
    
    def get_outgoing_traffic(self):
        return self.get_traffic(self.outgoing_traffic_id)

    def get_total_traffic(self, source):
        for result in source:
            if self.my_dict and result[0] in self.my_dict.keys():
                self.my_dict[result[0]] += int(result[1])
            else:
                self.my_dict[result[0]] = int(result[1])
        return self.my_dict
    
    def merge_traffic(self, source1, source2):
        final_result = list()
        i = 0
        while i < len(source1):
            tmp = list()
            tmp = source1[i]
            tmp = tmp + (source2[i][1],)
            final_result.append(tmp)
            i += 1
        return final_result
    
    def build_json(self, final_result):
        print("Merged Traffic")
        dict_obj = {self.traffic_tag: {"name": "", "utc": True, "columns": ["time", "in, out"],
                            "points": final_result}}
        # dict_obj = {"SAX": {"name": "", "utc": True, "columns": ["time", "in, out"],
        #                    "points": final_result}}

        r = json.dumps(dict_obj)
        loaded_r = json.loads(r)
        print(r)
