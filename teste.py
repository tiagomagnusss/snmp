# from user import User
# import time

# user = User('192.168.0.10', 'MD5DESUser', "testePassword", 'MD5', 'DES')
# times = 0

# time_start = time.time()
# user.updateData()
# time.sleep(5)
# user.updateData()
# time.sleep(5)
# user.updateData()
# time.sleep(5)
# user.updateData()
# time.sleep(5)
# user.updateData()
# time.sleep(5)
# user.updateData()
# time.sleep(5)
# user.updateData()
# time_end = time.time()



# for i in range(len(user.data[user.tag_dic['tcpInSegs']])):
#     print(user.data[user.tag_dic['tcpInSegs']][i])
# user.getDataInTime(time_start, time_end, 'tcpInSegs')

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

# from datetime import datetime
# import time

# date_string = "23/02/2023 12:50:00"


# print(datetime.strptime(date_string, "%d/%m/%Y %H:%M:%S").timestamp())
# print(time.time())

import matplotlib.pyplot as plt
from scipy import stats

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
y = [269.44, 620.48, 269.44, 483.2, 722.24, 483.2, 474.24, 483.2, 269.44, 483.2, 269.44, 483.2, 479.36, 755.52, 269.44, 483.2, 269.44, 483.2, 269.44, 483.2, 269.44, 483.2, 269.44, 269.44, 483.2, 801.28, 269.44, 269.44, 483.2, 269.44, 483.2, 483.2, 269.44, 269.44, 483.2, 269.44, 483.2]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()