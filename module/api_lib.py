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
        if params:
            params['_format'] = 'json'
        data = urllib.urlencode(params or {})

        request = urllib2.Request(config['url'], data, {'Content-Type': 'application/x-www-form-urlencoded'})
        request.get_method = lambda: config['method']
        request.add_header("Authorization", "Basic %s" % login_config.authentication)

        response = urllib2.urlopen(request).read()
        json_response = json.loads(response)

        print "%s %s" % (config['method'], config['url'])
        print "%s %s" % (json_response['codigo'], json_response['mensaje'])
        if len(json_response['error']) > 0:
            print json_response['error']

        return json_response

    def __repr__(self):
        return str(self.attrs)


class APISensor(APIEndpoint):
    config = endpoints_config.sensor

    @classmethod
    def create(cls, attrs):
        response = cls.request(cls.config['create'], attrs)
        return cls(response['datos'])

    @classmethod
    def change_state(cls):
        # TODO
        return

    @classmethod
    def get(cls, sensor_id):
        get_config = cls.config['get'].copy()
        get_config['url'] = get_config['url'].replace('{id}', str(sensor_id))
        response = cls.request(get_config)
        return cls(response['datos'])

    @classmethod
    def get_all(cls):
        response = cls.request(cls.config['get_all'])
        sensors = []
        for sensor in response['datos']:
            sensors.append(cls(sensor))
        return sensors

    @classmethod
    def delete(cls):
        # TODO
        return

    @classmethod
    def update(cls):
        # TODO
        return

    @classmethod
    def get_all_with_datatypes(cls):
        # TODO
        return

    def __str__(self):
        return 'Sensor<%d, %s>' % (self.attrs['id'], self.attrs['nombre'])