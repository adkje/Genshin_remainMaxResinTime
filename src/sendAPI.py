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
    
    def extract_datas(self):
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
        
    def refine_used_time(self):
        # 完全回復までにかかる時間
        int_resin_minute = int(self.necessaryData["resin_recovery_time"])
        nowDate = datetime.datetime.today()
        addTime = datetime.timedelta(seconds=int_resin_minute)

        eightMinute = 8 * 60
        sleepTime = int_resin_minute % eightMinute

        resin_recovered_time = nowDate + addTime
        resin_recovered_date = resin_recovered_time.strftime("%m月%d日 %H:%M:%S")

        return [sleepTime,resin_recovered_date]
    
    def gather_process(self):
        self.send_API()
        # 未加工状態で使えるデータを収納
        self.extract_datas()
        retouchedData = self.refine_used_time()
        # 加工状態で使えるデータを追加収納
        self.necessaryData.update(sleeptime=retouchedData[0],recovered_date=retouchedData[1])
        return self.necessaryData



