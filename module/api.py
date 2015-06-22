import endpoints_config
import login_config
import urllib
import urllib2
import json
import sys


class Endpoint:
    config = {}
    actions = ['create', 'get', 'get_all', 'delete', 'update']

    def __init__(self, attrs):
        self.attrs = attrs
        self.actions = ['save', 'remove']

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
            raise ValueError(str(json_response['error']) + '\n')

        return json_response

    # --Generic methods --

    @classmethod
    def create(cls, attrs=None):
        response = cls.request(cls.config['create'], attrs)
        return cls(response['datos'])

    @classmethod
    def get(cls, obj_id):
        get_config = cls.config['get'].copy()
        get_config['url'] = get_config['url'].replace('{id}', str(obj_id))
        response = cls.request(get_config)
        return cls(response['datos'])

    @classmethod
    def get_all(cls):
        response = cls.request(cls.config['get_all'])
        objects = []
        for obj in response['datos']:
            objects.append(cls(obj))
        return objects

    @classmethod
    def delete(cls, obj_id):
        delete_config = cls.config['delete'].copy()
        delete_config['url'] = delete_config['url'].replace('{id}', str(obj_id))
        response = cls.request(delete_config)
        return response

    @classmethod
    def update(cls, params):
        update_config = cls.config['update'].copy()
        update_config['url'] = update_config['url'].replace('{id}', str(params['id']))
        response = cls.request(update_config, params)
        return response

    def save(self):
        return self.update(self.attrs)

    def remove(self):
        return self.delete(self.attrs['id'])


class Account(Endpoint):
    config = endpoints_config.account

    def __repr__(self):
        return 'Cuenta<%d, %s>' % (self.attrs['id'], self.attrs['nombre'])


class Sensor(Endpoint):
    config = endpoints_config.sensor
    actions = Endpoint.actions + ['change_state', 'get_all_with_datatypes']

    @classmethod
    def change_state(cls, params):
        response = cls.request(cls.config['change_state'], params)
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


class DataType(Endpoint):
    config = endpoints_config.datatype
    actions = ['create', 'get', 'update', 'get_from_sensor_type', 'get_from_sensor']

    @classmethod
    def get_from_sensor_type(cls, sensor_type_id):
        get_config = cls.config['get_from_sensor_type'].copy()
        get_config['url'] = get_config['url'].replace('{id}', sensor_type_id)
        response = cls.request(get_config)
        datatypes = []
        for datatype in response['datos']:
            datatypes.append(cls(datatype))
        return datatypes

    @classmethod
    def get_from_sensor(cls, sensor_id):
        get_config = cls.config['get_from_sensor'].copy()
        get_config['url'] = get_config['url'].replace('{id}', sensor_id)
        response = cls.request(get_config)
        datatypes = []
        for datatype in response['datos']:
            datatypes.append(cls(datatype))
        return datatypes
