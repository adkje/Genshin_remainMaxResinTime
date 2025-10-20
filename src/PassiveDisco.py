import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from string import Template
import json

from sendAPI import requestAPI
import GenshinAPIList as Glist

message_json = None
with open("src/message.json", "r", encoding="utf-8") as f:
        message_json = json.load(f)
maxResinTime = Template(message_json["resinRelated"]["maxResinTime"])
dailyCompletion = message_json["dailyRelated"]["dailyCompletion"]
dailyIncompletion = message_json["dailyRelated"]["dailyIncompletion"]
botStop = message_json["errorMessage"]["botStop"]

def getSendMessages():
    return {"maxResinTime": maxResinTime,
            "dailyCompletion": dailyCompletion,
            "dailyIncompletion": dailyIncompletion,
            "botStop": botStop}

class PassiveAuto(requestAPI):
    # def __init__(self, name, cookies, uid, sendUser):
    def __init__(self, name, cookies, uid, client, discordId):
        super().__init__(name, cookies, uid,)
        self.client = client
        self.discordId = discordId
        self.messages = getSendMessages()


    async def korosuzo(self):
        # requireDataはwhile_processで定義。
        if self.requiredData["current_resin"] == 132:
            messages = getSendMessages()
            message = messages["maxResinTime"].substitute(currentResin=self.requiredData["current_resin"], recoveryTime=self.requiredData["recovered_date"])
            await self.sendUser.send(f"おはよう{message}" )
        # await asyncio.sleep(self.requiredData["sleeptime"])


    async def dailySend(self):

        if self.requiredData["is_extra_task_reward_received"] == False:
            await self.sendUser.send(f"{self.messages["dailyIncompletion"]}")

        else:
            await self.sendUser.send(f"{self.messages["dailyCompletion"]}")
    
    async def errorHundRing(self):
        messages = await getSendMessages()
        await self.sendUser.send(f"{self.messages["botStop"]}")

    async def dailyScheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.dailySend, 'cron', hour=3, minute=15)
        scheduler.start()
        await asyncio.Event().wait()

    async def auto_send_message_to_user(self):
        self.sendUser = await self.client.fetch_user(self.discordId)
        asyncio.create_task(self.dailyScheduler())
        while True:
            try:   
                self.requiredData = super().gather_process()
                await self.korosuzo()
                await asyncio.sleep(self.requiredData["sleeptime"])
            except Exception as e:
                await self.errorHundRing()
                await asyncio.sleep(3600)




class PassiveManual(requestAPI):
    def __init__(self, name, cookies, uid, client, discordId):
        super().__init__(name, cookies, uid,)
        self.client = client
        self.discordId = discordId
        self.messages = getSendMessages()

    async def sendManualMessage(self,message,userInstance,):
        # current_resin = userInstance.requiredData["current_resin"]
        # recovered_date = userInstance.requiredData["recovered_date"]
        is_extra_task_reqard_received = userInstance.requiredData["is_extra_task_reward_received"]
        
        if message.content.startswith('$getresin'):
            messages = getSendMessages()
            message = messages["maxResinTime"].substitute(currentResin=userInstance.requiredData["current_resin"], recoveryTime=userInstance.requiredData["recovered_date"])
            await userInstance.sendUser.send(f"{message}" )

        if message.content.startswith('$dailymission'):
            # PassiveAutoをリファクタリングして同一コードをコンポーネント化できる。
            messages = getSendMessages()
            if is_extra_task_reqard_received == False:
                await userInstance.sendUser.send(f"{messages["dailyIncompletion"]}")

            else:
                await userInstance.sendUser.send(f"{messages["dailyCompletion"]}")

    async def getValueOfClass(self,message):

        if not message.content.startswith(('$getresin','$dailymission')):
            return
        
        # type int
        for i in range(0,len(Glist.User)):
            if message.author.id == Glist.User.get(f"User{i}").get("discordId"):
                # classObjectにはPassiveAutoが格納されている。
                userInstance = Glist.User[f"User{i}"]["classObject"]
                await self.sendManualMessage(message,userInstance)
                break
                                        
            elif None == Glist.User.get(f"User{i}").get("discordId"):
                await userInstance.sendUser.send("ユーザー登録をしてください！")
    
    
            