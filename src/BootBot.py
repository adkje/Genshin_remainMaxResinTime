
from PassiveDisco import PassiveAuto
# from PassiveDisco import bot_ready

import discord
import asyncio
import os

import GenshinAPIList as Glist
    
# This example requires the 'message_content' intent.

bot_ready = asyncio.Event()
allUser = []
# 面倒になっちゃった。

class Bot(discord.Client):

    async def on_ready(self):
        print(f'We have logged in as {client.user}')
        await bot_ready.set()
        
    async def on_message(self,message):
        if message.author == client.user:
            return
        print("message着弾")
        # 1.特定のメッセージか否か,2.そのユーザーが存在するか,3
    
        if message.content.startswith('$test'):
            print("testです。")
            # type int
            print(type(message.author.id))
            for i in range(0,len(Glist.User)):

                if bool(Glist.User.get(f"User{i}").get("discordId")):

                    if message.author.id == Glist.User[f"User{i}"]["discordId"]:
                        userInstance = Glist.User[f"User{i}"]["classObject"]
                        current_resin = userInstance.requiredData["current_resin"]
                        recovered_date = userInstance.requiredData["recovered_date"]
                        await userInstance.sendUser.send(f"現在の樹脂は{current_resin}です！200に達するまで{recovered_date}分です！" )

                        break
                                    
                else:
                    await userInstance.sendUser.send("ユーザー登録をしてください！")


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
    await userClassObject.korosuzo()

async def BootBot():
    await client.start(os.environ["Distoken"])

async def gather():
    await asyncio.gather(BootBot(),*(fire(classObject) for classObject in allUser))

    
asyncio.run(gather())
# print(Glist.User)
