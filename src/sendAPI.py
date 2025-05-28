import requests
import datetime
import asyncio

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
        print("SendAPI実行")
        return self.Receive_response
    
    def extract(self,jsondata):
        data = jsondata["data"]

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
        
    def retouch(self):
        # 完全回復までにかかる時間
        int_resin_minute = int(self.necessaryData["resin_recovery_time"])
        nowDate = datetime.datetime.today()
        addTime = datetime.timedelta(seconds=int_resin_minute)

        recover_date = nowDate + addTime
        eightMinute = 8 * 60
        sleeptime = int_resin_minute % eightMinute
        
        return sleeptime,recover_date

User1info = Glist.User["User1"]
User1 = requestAPI(User1info["name"],User1info["Cookies"],User1info["uid"])

async def while_process(User):
            print("while_process始まり")
            Receive_response = User.send_API()
            User.extract(Receive_response)
            recover_date = User.retouch()
            print(f"次の回復時間は{recover_date}秒です。")
            await asyncio.sleep(recover_date)
            print("as;lfkjas;f")
            return recover_date

# print(while_process(User1))
if __name__ == "__main__":
    asyncio.run(while_process(User1))
