
import discord
import asyncio
import os

import GenshinAPIList as Glist
from PassiveDisco import PassiveAuto
from PassiveDisco import PassiveManual

# This example requires the 'message_content' intent.
# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# os.environを用いて環境変数を表示させます
bot_ready = asyncio.Event()
allUser = []
# 面倒になっちゃった。

class Bot(discord.Client,PassiveManual):
    async def on_ready(self):
        print(f'We have logged in as {client.user}')
        await bot_ready.set()
        
    async def on_message(self,message):
        if message.author == client.user:
            return
        print("message着弾")
        await self.getValueOfClass(message)

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)

# async def define(discordId):

#     return sendUser


for i in range(0,len(Glist.User)):
        User = Glist.User[f"User{i}"]
        print(f"これは20行目です。{i}")
        discordId = User["discordId"]
        # sendUser = asyncio.run(define(discordId))

        User["classObject"] = PassiveAuto(User["name"],User["Cookies"],User["uid"],client,discordId)
        allUser.append(User["classObject"])



async def fire(userClassObject):
    await bot_ready.wait()
    await userClassObject.while_process()

async def BootBot():
    await client.start(os.environ["Distoken"])

async def gather():
    await asyncio.gather(BootBot(),*(fire(classObject) for classObject in allUser))
    
asyncio.run(gather())