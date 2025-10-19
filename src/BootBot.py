
import discord
import asyncio
import os
from dotenv import load_dotenv

import GenshinAPIList as Glist
from PassiveDisco import getSendMessages
from PassiveDisco import PassiveAuto
from PassiveDisco import PassiveManual



load_dotenv()

bot_ready = asyncio.Event()
UserClass = []

class Bot(discord.Client,PassiveManual):
    async def on_ready(self):
        print(f'We have logged in as {client.user}')
        # # 一度だけjsonを読み込ませたいため、最初はjsonの内容をNoneと定義しておく。
        # await getSendMessages()
        await bot_ready.set()
        
    async def on_message(self,message):
        if message.author == client.user:
            return
        await self.getValueOfClass(message)

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)

# async def define(discordId):

#     return sendUser


for i in range(0,len(Glist.User)):
        User = Glist.User[f"User{i}"]
        discordId = User["discordId"]
        # sendUser = asyncio.run(define(discordId))

        User["classObject"] = PassiveAuto(User["name"],User["Cookies"],User["uid"],client,discordId)
        UserClass.append(User["classObject"])



async def fire(userClassObject):
    await bot_ready.wait()
    await userClassObject.auto_send_message_to_user()

async def BootBot():
    await client.start(os.environ["Distoken"])

async def gather():
    await asyncio.gather(BootBot(),*(fire(classObject) for classObject in UserClass))
    
asyncio.run(gather())