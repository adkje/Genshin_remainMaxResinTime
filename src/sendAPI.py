import requests
import datetime

import GenshinAPIList as Glist

url = "https://bbs-api-os.hoyoverse.com/game_record/genshin/api/dailyNote"
class requestAPI:
    def __init__(self,name,cookies,uid):
        self.name = name
        self.cookies = cookies
        self.uid = uid

        self.params =  {
                          "role_id": f"{self.uid}",
                          "server": 'os_asia',
                          "schedule_type": 1,
                        }
    
    def send_API(self):
        self.Receive_response = requests.get(url, cookies = self.cookies, params = self.params).json()
    
    def extract(self):
        data = self.Receive_response["data"]

        current_resin = data["current_resin"]
        max_resin = data["max_resin"]
        resin_recovery_time = data["resin_recovery_time"]
        is_extra_task_reward_received = data["is_extra_task_reward_received"]

        self.necessaryData = {
            "current_resin" : current_resin,
            "max_resin" : max_resin,
            "resin_recovery_time" : resin_recovery_time,
            "is_extra_task_reward_received" :is_extra_task_reward_received,
        }
        return self.necessaryData
        
    def retouch(self):
        # 完全回復までにかかる時間
        int_resin_minute = int(self.necessaryData["resin_recovery_time"])
        nowDate = datetime.datetime.today()
        addTime = datetime.timedelta(seconds=int_resin_minute)

        eightMinute = 8 * 60
        sleeptime = int_resin_minute % eightMinute

        recovered_date = nowDate + addTime
        recovered_date = recovered_date.replace(microsecond = 0)
        recovered_date = recovered_date.strftime("%m月%d日 %H:%M:%S")

        retouchedData = [sleeptime,recovered_date]
        return retouchedData
    
    def gather_process(self):
        self.send_API()
        # 未加工状態で使えるデータを収納
        self.extract()
        retouchedData = self.retouch()
        # 加工状態で使えるデータを追加収納
        self.necessaryData.update(sleeptime=retouchedData[0],recovered_date=retouchedData[1])
        return self.necessaryData



