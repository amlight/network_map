from pyzabbix import ZabbixAPI
from zabbix import *
import time
import json
from datetime import datetime
import os.path
from os import path


class TrafficAnalyzer:

    def __init__(self, in_traffic_tag, in_incoming_traffic_id, in_outgoing_traffic_id):

        self.traffic_tag = in_traffic_tag
        self.incoming_traffic_id = in_incoming_traffic_id
        self.outgoing_traffic_id = in_outgoing_traffic_id

        self.final_result = list()

        """
        Zabbix API Credentials
        """
        self.zabbix = Zabbix()

        self.ZABBIX_SERVER = self.zabbix.ZABBIX_SERVER
        self.ZABBIX_USER = self.zabbix.ZABBIX_USER
        self.ZABBIX_PSSW = self.zabbix.ZABBIX_PSSW

        self.zapi = ZabbixAPI(self.ZABBIX_SERVER)
        self.zapi.login(self.ZABBIX_USER, self.ZABBIX_PSSW)

        """
        Time frame to be considered
        """
        self.time_till = time.mktime(datetime.now().timetuple())
        self.time_from = self.time_till - 60 * 60 * 1  # last 1 hours

        if path.exists('data_file.json'):
            os.remove('data_file.json')

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
            tmp = (source1[i][0], source1[i][1], source2[i][1])
            self.final_result.append(tmp)
            i += 1

    """
        Method to create a json object given the tag name and the points list
    """

    def build_json(self, tag, points):
        dict_obj = {tag: {"name": "", "utc": True, "columns": ["time", "in", "out"],
                          "points": points}}
        r = json.dumps(dict_obj)

        if path.exists('data_file.json'):
            data = dict()
            with open("data_file.json", 'r+') as write_file:
                old_data = json.load(write_file)
                data = dict(old_data)
                data.update(dict_obj)

            with open("data_file.json", 'r+') as write_file:
                json.dump(data, write_file)
        else:
            with open("data_file.json", 'w+') as write_file:
                json.dump(dict_obj, write_file)

        write_file.close()
        print(r)

    """
        Compute the incoming traffic and outgoing traffic, merge both information in a same data structure
        and send that result to be structured as a JSON
    """

    def traffic_on_json(self):

        # Incoming Traffic
        results1 = self.get_traffic('in')

        # Outgoing Traffic
        results2 = self.get_traffic('out')

        self.merge_traffic(results1, results2)

        print("Merged Traffic")
        self.build_json(self.traffic_tag, self.final_result)

        return self.final_result

    """
        Method to compute the total traffic between two points
    """

    def total_traffic(self, source1, source2):
        i = 0
        out_total_traffic = list()
        while i < len(source1):
            tmp = (source2[i][0], source1[i][1] + source2[i][1], source1[i][2] + source2[i][2])
            out_total_traffic.append(tmp)
            i += 1

        print("Total Traffic")
        self.build_json("Total", out_total_traffic)
