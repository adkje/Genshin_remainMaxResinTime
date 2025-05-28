from SendAPI import requestAPI
from SendAPI import while_process
import discord
import asyncio
import os

import GenshinAPIList as Glist
    
# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class Bot(discord.Client):
    
    async def on_ready(self):
        print(f'We have logged in as {client.user}')

    async def on_message(self,message):
        if message.author == client.user:
            return
        print("message着弾")
        
        user_id = message.author.id

        if message.content.startswith('$test'):
            print("testです。")

            for i in (range(1,2)):
                print("判定中")
                userDic = Glist.User[f"User{i}"]
                discordIdDic = userDic["DiscordID"]

                if discordIdDic == user_id:
                    print("同じです。")
                    userDic["ClassObject"] = requestAPI(userDic["name"],userDic["Cookies"],userDic["uid"])
                    break
                    # return userDic
            
            await while_process(userDic["ClassObject"])
            # User
            await message.channel.send('Hello!')


intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
async def BootBot():
    await client.start(os.environ["Distoken"])

asyncio.run(BootBot())
print(Glist.User)
