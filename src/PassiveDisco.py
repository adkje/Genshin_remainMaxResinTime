import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from SendAPI import requestAPI
import GenshinAPIList as Glist


class PassiveAuto(requestAPI):
    # def __init__(self, name, cookies, uid, sendUser):
    def __init__(self, name, cookies, uid, client, discordId):
        super().__init__(name, cookies, uid,)
        self.client = client
        self.discordId = discordId


    async def korosuzo(self):
            # 最後に送るところでエラー吐いている。
        # requireDataはwhile_processで定義。
        if self.requiredData["current_resin"] == 180:
            await self.sendUser.send(f"PassiveDisco現在の樹脂は{self.requiredData["current_resin"]}です！200に達するまで{self.requiredData["recovered_date"]}です！" )
        # await asyncio.sleep(self.requiredData["sleeptime"])


    async def dailySend(self):

        if self.requiredData["is_extra_task_reward_received"] == False:
            # await self.sendUser.send("デイリー任務が未完了です。")
            await self.sendUser.send("デイリー任務が未完了です。")

        else:
            await self.sendUser.send("デイリー任務を完了しています。")


        
    async def dailyScheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.dailySend, 'cron', hour=23, minute=00)
        scheduler.start()
        await asyncio.Event().wait()

    async def while_process(self):

        self.sendUser = await self.client.fetch_user(self.discordId)
        print("while_processです")
        asyncio.create_task(self.dailyScheduler())
        while True:

            self.requiredData = super().gather_process()

            await self.korosuzo()
            # await self.dailySend()
            print(self.requiredData["sleeptime"])
            print(self.requiredData["is_extra_task_reward_received"])
            await asyncio.sleep(self.requiredData["sleeptime"])

class PassiveManual(requestAPI):
    async def sendManualMessage(self,message,userInstance,):
        current_resin = userInstance.requiredData["current_resin"]
        recovered_date = userInstance.requiredData["recovered_date"]
        is_extra_task_reqard_received = userInstance.requiredData["is_extra_task_reward_received"]
        
        if message.content.startswith('$getresintest'):
            await userInstance.sendUser.send(f"BootBot現在の樹脂は{current_resin}です！200に達するまで{recovered_date}です！" )

        if message.content.startswith('$dailymissiontest'):
            # PassiveAutoをリファクタリングして同一コードをコンポーネント化できる。
            if is_extra_task_reqard_received == False:
                # await self.sendUser.send("デイリー任務が未完了です。")
                await userInstance.sendUser.send("デイリー任務が未完了です。")

            else:
                await userInstance.sendUser.send("デイリー任務を完了しています。")

    async def getValueOfClass(self,message):
        # type int
        print("getValue")
        for i in range(0,len(Glist.User)):
            print("infor")
            if message.content.startswith(('$getresintest','$dailymissiontest')):
                print("instart")
                if message.author.id == Glist.User.get(f"User{i}").get("discordId"):
                    print("indiscord")
                    # classObjectにはPassiveAutoが格納されている。
                    userInstance = Glist.User[f"User{i}"]["classObject"]
                    await self.sendManualMessage(message,userInstance)

                    break
                                        
                elif None == Glist.User.get(f"User{i}").get("discordId"):
                    await userInstance.sendUser.send("ユーザー登録をしてください！")
    
    
            