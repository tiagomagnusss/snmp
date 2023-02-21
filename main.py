from easysnmp import Session
import datetime
import time
from tcp import TCP

hostname = 'localhost'
community = 'public'
version = 3
user = 'rwrite'
pw = ''
auth_protocol = 'MD5'
privacy_protocol = 'DES'

session = Session(
    hostname=hostname,
    version=version,
    security_level='auth_with_privacy',
    security_username=user,
    auth_protocol=auth_protocol,
    auth_password=pw,
    privacy_protocol=privacy_protocol,
    privacy_password=pw
)

tcp = TCP(session)
ts = int(time.time())
x = tcp.get_data()
print(x)
