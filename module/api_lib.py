import endpoints_config
import login_config
import urllib
import urllib2
import json
# import time
# import httplib
# import os
# from datetime import datetime
# import types


class APIEndpoint:
    def __init__(self, attrs):
        self.attrs = attrs

    @staticmethod
    def request(config, params=None):
        request = urllib2.Request(config['url'])
        request.get_method = lambda: config['method'].upper()
        request.add_header("Authorization", "Basic %s" % login_config.authentication)
        query_args = urllib.urlencode(params or {})
        request.add_data(query_args)

        response = urllib2.urlopen(request).read()
        json_response = json.loads(response)
        return json_response

    def __repr__(self):
        return str(self.attrs)


class APISensor(APIEndpoint):
    config = endpoints_config.sensor

    @classmethod
    def get_all(cls):
        response = cls.request(cls.config['get_all'])
        sensors = []
        for sensor in response['datos']:
            sensors.append(cls(sensor))
        return sensors
