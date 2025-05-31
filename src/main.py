allUser = []
# 面倒になっちゃった。
for i in range(0,len(Glist.User)):
        User = Glist.User[f"User{i}"]
        print(f"これは20行目です。{i}")
        discordId = User["DiscordID"]
        discordUser = client.get_user(discordId)

        User["ClassObject"] = PassiveAuto(User["name"],User["Cookies"],User["uid"],discordUser)
        allUser.append(User["ClassObject"])




async def while_process(User,discordID):
                
        while(True):
            user = client.get_user(discordID)
            userDic = Glist.User[f"User{i}"]
            userDic["ClassObject"] = PassiveAuto(User["name"],User["Cookies"],User["uid"],user)
            Receive_response = User.send_API()
            User.extract(Receive_response)
            recover_date = User.retouch()
            print(f"次の回復時間は{recover_date}秒です。")
            await asyncio.sleep(recover_date)

async def BootBot():
    await client.start(os.environ["Distoken"])

asyncio.gather(BootBot(),while_process())
asyncio.run(BootBot())
print(Glist.User)
