import datetime


time1=datetime.datetime.now()
time1_str = datetime.datetime.strftime(time1,'%Y-%m-%d-%H-%M')


print(time1_str)