

class Passive():
    async def aiueo(client,message):
        
        print("メッセを受け取りました。")
        if message.author == client.user:
            return
        

        # if message.content.startswith('$getresin'):
        #     kekka = await SendAPI.one_process(SendAPI.User1)
        #     # await BootBot.SendUser.message.send(f"現在の樹脂は{main.nowresin}です！200に達するまで{main.UntilTwoHundred}分です！")
        #     await message.channel.send(f"現在の樹脂は{kekka[3]}です！200に達するまで{kekka[1]}分です！")

        # if message.content.startswith('$hello'):
            # await message.channel.send('Hello!')




