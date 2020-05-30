import datetime
from datetime import datetime, timedelta

# date_aot = str(datetime.today())[0:10]
#
# days = date_aot[-2:]
# day = int(date_aot[-2:])
#     day = 9
#     if day <= 9:
#         day = day[-1]
# print(day)
import os

num = '09'
county = "los-angeles"
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path + '/csv/' + county + '.csv'

print(dir_path)