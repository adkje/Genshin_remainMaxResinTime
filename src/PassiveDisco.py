import asyncio
from SendAPI import requestAPI

import GenshinAPIList as Glist
import discord




class PassiveAuto(requestAPI):
    # def __init__(self, name, cookies, uid, sendUser):
    def __init__(self, name, cookies, uid, client, discordId):
        super().__init__(name, cookies, uid,)
        self.client = client
        self.discordId = discordId


    async def korosuzo(self):
        # API = requestAPI(self.name,self.cookies,self.uid)
        self.sendUser = await self.client.fetch_user(self.discordId)
        # 未発火
        self.requiredData = super().gather_process()
        # 最後に送るところでエラー吐いている。
        print(self.requiredData)
        await self.sendUser.send(f"現在の樹脂は{self.requiredData["current_resin"]}です！200に達するまで{self.requiredData["recovered_date"]}分です！" )
        await asyncio.sleep(self.requiredData["sleeptime"])




