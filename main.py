import discord
import logging
import pickle
import asyncio
import os
import sys

logging.basicConfig(level=logging.INFO)
command = "!"
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
        if all in message.content:
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
        print('Logged on as {0}!'.format(self.user))
        await client.change_presence(activity=discord.Game(name='documentation'))

    def check_if_it_is_me(message: discord.Message):
        return message.author.id == int(owner)

    async def on_message(self, message: discord.Message):
        if message.content.startswith(command):
            if MyClient.check_if_it_is_me(message):
                mute(message)
        await removeMessages(message)
        print('Message from {0.author}: {0.content}'.format(message))


if __name__ == '__main__':
    print(muteList)
    client = MyClient()
    client.run(token)
