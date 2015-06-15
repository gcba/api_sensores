base_url = "https://apisensores.buenosaires.gob.ar/app_dev.php"
sensor = {
    "change_state": {
        "method": "PUT",
        "url": "%s/api/sensor/cambiarestado" % base_url
    },
    "create": {
        "method": "POST",
        "url": "%s/api/sensor/create" % base_url
    },
    "get": {
        "method": "GET",
        "url": "%s/api/sensor/{id}" % base_url
    },
    "delete": {
        "method": "PUT",
        "url": "%s/api/sensor/{id}/baja" % base_url
    },
    "update": {
        "method": "PUT",
        "url": "%s/api/sensor/{id}/update" % base_url
    },
    "get_all": {
        "method": "GET",
        "url": "%s/api/sensores" % base_url
    },
    "get_all_with_datatypes": {
        "method": "GET",
        "url": "%s/api/sensorestipodato" % base_url
    }
}
