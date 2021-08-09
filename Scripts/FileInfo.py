import datetime
import os
import requests

print("Input the FILENAME with its' PATH: ")
filename = input()
# 文件大小
filesize = os.path.getsize(filename)
print(filesize)

# 创建日期
create_time = os.path.getctime(filename)
print(datetime.datetime.fromtimestamp(create_time))

# 最近修改时间
modify_time = os.path.getmtime(filename)
print(datetime.datetime.fromtimestamp(modify_time))
