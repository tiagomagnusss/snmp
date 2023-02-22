from user import User
import time

user = User('192.168.0.10', 'MD5DESUser', "testePassword", 'MD5', 'DES')
times = 0

time_start = time.time()
user.updateData()
time.sleep(5)
user.updateData()
time.sleep(5)
user.updateData()
time.sleep(5)
user.updateData()
time.sleep(5)
user.updateData()
time.sleep(5)
user.updateData()
time.sleep(5)
user.updateData()
time_end = time.time()



for i in range(len(user.data[user.tag_dic['tcpInSegs']])):
    print(user.data[user.tag_dic['tcpInSegs']][i])
user.getDataInTime(time_start, time_end, 'tcpInSegs')

# while(1):
#     user.updateData()
#     data = user.getTaxa('udpOutDatagrams')
#     time.sleep(1)

# while(1):
#     user.updateData()
#     data = user.data
#     print("frame: ", times)
#     times += 1
#     print('------------------------------------------------')
#     user.getTaxa('udpInDatagrams')
#     user.getTaxa('udpOutDatagrams')
#     user.getTaxa('tcpInSegs')
#     user.getTaxa('tcpOutSegs')
#     print('------------------------------------------------')
#     for i in range(len(data)):
#         #print(data[i])
#         print(data[i][len(data[i])-1]['tag'], ': ', data[i][len(data[i])-1]['data'])
#     print('------------------------------------------------')
#     time.sleep(1)