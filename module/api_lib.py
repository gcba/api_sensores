import endpoints_config
import login_config
import urllib
import urllib2
import json
import sys
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

        sys.stdout.write("%s %s\n" % (config['method'], config['url']))
        sys.stdout.write("%s %s\n" % (json_response['codigo'], json_response['mensaje']))
        if len(json_response['error']) > 0:
            sys.stdout.write(json_response['error'] + '\n')

        return json_response


class APISensor(APIEndpoint):
    config = endpoints_config.sensor

    @classmethod
    def create(cls, attrs):
        response = cls.request(cls.config['create'], attrs)
        return cls(response['datos'])

    @classmethod
    def change_state(cls, params):
        response = cls.request(cls.config['change_state'], params)
        return response

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
    def delete(cls, params):
        response = cls.request(cls.config['delete'], params)
        return response

    @classmethod
    def update(cls, params):
        response = cls.request(cls.config['update'], params)
        return response

    @classmethod
    def get_all_with_datatypes(cls):
        response = cls.request(cls.config['get_all_with_datatypes'])
        sensors = []
        for sensor in response['datos']:
            sensors.append(cls(sensor))
        return sensors

    def __repr__(self):
        return 'Sensor<%d, %s>' % (self.attrs['id'], self.attrs['nombre'])
