import base64

username = 'USER'
password = 'PASS'
authentication = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
