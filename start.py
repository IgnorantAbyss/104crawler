import os
import csv

from module import GetJobInfo
from module import GetJobList
# from module import GetJobInfo
# from module import GetJobList


# 確保結果資料夾存在
if not os.path.exists('result'):
    os.makedirs('result')

location_dict = {
    "台北市":6001001000,
    "新北市":6001002000,
    "宜蘭縣":6001003000,
    "基隆市":6001004000,
    "桃園市":6001005000,
    "新竹縣市":6001006000,
    "苗栗縣":6001007000,
    "台中市":6001008000,
    "彰化縣":6001010000,
    "南投縣":6001011000,
    "雲林縣":6001012000,
    "嘉義縣市":6001013000,
    "台南市":6001014000,
    "高雄市":6001016000,
    "屏東縣":6001018000,
    "台東縣":6001019000,
    "花蓮縣":6001020000,
    "澎湖縣":6001021000,
    "金門縣":6001022000,
    "連江縣":6001023000
    }

# 設定搜尋關鍵字
keyword = '數據工程師'

# 設定搜尋頁數
custom_pages = 1

for location, code in location_dict.items():
    job_list = GetJobList.get_job_list(keyword, location=location, custom_pages=custom_pages)
    # job_list = GetJobList.get_job_list(keyword, location=location)

    job_info_df = GetJobInfo.get_job_info(job_list=job_list)

    with open(fr'result\104{location} {keyword}1.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(job_info_df.columns)
        writer.writerows(job_info_df.values)