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
# import os
#
# num = '09'
# county = "los-angeles"
# dir_path = os.path.dirname(os.path.realpath(__file__))
# dir_path = dir_path + '/csv/' + county + '.csv'
#
# print(dir_path)

counties = ['Los Angeles', 'Riverside', 'San Diego', 'Orange', 'San Bernardi', 'Alameda', 'Santa Clara', 'San Francisco', 'San Mateo', 'Kern', 'Tulare', 'Santa Barbara', 'Fresno', 'Imperial', 'Contra Costa', 'Sacramento', 'Ventura', 'San Joaquin', 'Kings', 'Stanislaus', 'Sonoma', 'Solano', 'Monterey', 'Marin', 'Merced', 'San Luis Obispo', 'Yolo', 'Santa Cruz', 'Placer', 'Napa', 'Humboldt', 'Madera', 'El Dorado', 'San Benito', 'Del Norte', 'Sutter', 'Nevada', 'Butte', 'Shasta', 'Mono', 'Mendocino', 'Yuba', 'Lake', 'Inyo', 'Mariposa', 'Calaveras', 'Glenn', 'Amador', 'Siskiyou', 'Colusa', 'Lassen', 'Tehama', 'Plumas', 'Tuolumne', 'Alpine', 'Modoc', 'Sierra', 'Trinity', 'Alameda - Berk', 'Yuba-Sutter']
# counties = counties.sort()

print(sorted(counties))