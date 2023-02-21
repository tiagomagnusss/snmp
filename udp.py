# Primeiro precisamos importar a biblioteca do Easy SNMP
from easysnmp import Session
from datetime import datetime  
import time

session = Session(hostname='localhost', security_level="auth_with_privacy", security_username='MD5DESUser', auth_password="md51234567", auth_protocol='MD5', privacy_password="des1234567", privacy_protocol='DES', version=3)

t = 1

tx_udp_in = []
tx_udp_out = []

udp_in_prev = -1
udp_out_prev = -1

system_items = session.walk('udpInDatagrams')
init_udp_in = int(system_items[0].value)


system_items = session.walk('udpOutDatagrams')
init_udp_out = int(system_items[0].value)

# system_items = session.walk('udpOutDatagrams')
while 1:
    system_items = session.walk('udpInDatagrams')
    udp_in = int(system_items[0].value) - init_udp_in
    print('Udp in: ', udp_in)    
    
    system_items = session.walk('udpOutDatagrams')
    udp_out = int(system_items[0].value) - init_udp_out
    print('Udp out: ',udp_out)    

    if udp_in_prev > 1 and udp_out_prev > 1 :
        print('taxa in udp: ', ((udp_in-udp_in_prev)/1), 'd/s')
        print('taxa out udp: ', ((udp_out-udp_out_prev)/1), 'd/s')
        udp_in_prev = udp_in
        udp_out_prev = udp_out

    else :
        udp_in_prev = udp_in
        udp_out_prev = udp_out
    
    tx_udp_in.append([time.time(), udp_in])
    tx_udp_out.append([time.time(), udp_out])
    
    print('---------------------------------')
    # for i in range(len(tx_udp_in)):
    #     print( datetime.fromtimestamp(tx_udp_in[i][0]) , " ", tx_udp_in[i][1])
    
    # for i in range(len(tx_udp_out)):
    #     print( datetime.fromtimestamp(tx_udp_out[i][0]) , " ", tx_udp_out[i][1])

    # print('---------------------------------')
    time.sleep(t)

# system_items = session.walk('udpNoPorts')
# print('udpNoPorts: ',system_items[0].value)

# system_items = session.walk('udpInErrors')
# print('udpInErrors: ',system_items[0].value)


# system_items = session.walk('udpLocalPort')
# portas = []
# for i in range(len(system_items)):
#     portas.append(system_items[i].value)

# print('udpLocalPorts: ', portas)

# system_items = session.walk('icmp')
# print(system_items)

