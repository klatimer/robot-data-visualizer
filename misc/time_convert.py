import datetime

time = [1347517370111111]
time = time[:10]
time = datetime.datetime.fromtimestamp(time).strftime('%c')
print(time)