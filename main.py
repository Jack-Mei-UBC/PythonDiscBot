import discord
import logging
import pickle
import os
import functions.flag as flag

logging.basicConfig(level=logging.INFO)
command = "."
owner = "219905033876013058"
save = "data.pkl"
token = os.getenv("DISC_TOKEN")
with open(save, 'rb') as input:
    try:
        muteList = pickle.load(input)
        print("loaded")
    except:
        print("Failed to read")
        muteList = [];


def saving() -> None:
    with open(save, 'wb') as output:
        pickle.dump(muteList, output, pickle.HIGHEST_PROTOCOL)


def mute(message: discord.Message):
    if message.content.startswith(command + "mute"):
        for members in message.mentions:
            if members.id not in muteList:
                muteList.append(members.id)
                print(members.id)
        saving()


def unMute(message: discord.Message):
    if message.content.startswith(command + "unmute"):
        for members in message.mentions:
            if members.id in muteList:
                muteList.remove(members.id)
                print(members.id)
        if "all" in message.content:
            muteList.clear()
        saving()


async def removeMessages(message: discord.Message):
    for members in muteList:
        print("checking")
        if message.author.id == members:
            print('Deleted message from {0.author}: {0.content}'.format(message))
            await message.delete()


class MyClient(discord.Client):
    async def on_ready(self):
        flag.startWeekly()
        print('Logged on as {0}!'.format(self.user))
        await client.change_presence(activity=None)

    def check_if_it_is_me(message: discord.Message) -> None:
        return message.author.id == int(owner)

    async def on_message(self, message: discord.Message) -> None:
        if message.content.startswith(command):
            if MyClient.check_if_it_is_me(message):
                mute(message)
                unMute(message)
            if str(message.channel) == "bot-commands" or str(message.channel) == "flag-race" or str(message.channel) == "testing":
                if message.content.startswith(command + "flag"):
                    flag.addScore(message.author, str(message.content))
                elif message.content.startswith(command + "leaderboards"):
                    await message.channel.send(embed = flag.returnScoreBoard())
                elif message.content.startswith(command + "edit"):
                    flag.editScore(message.author, str(message.content), message.mentions)
                elif message.content.startswith(command + "stats"):
                    await message.channel.send(embed = flag.returnIndividual(message.author))

        await removeMessages(message)


if __name__ == '__main__':
    print(muteList)
    client = MyClient()
    client.run(token)
