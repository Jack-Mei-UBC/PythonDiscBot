import pandas as pd
import os
import discord
from datetime import datetime, timedelta, timezone


def save(data: [[discord.Member, [int]]]):
    dir_path = os.getcwd()
    data = [[person[0].id] + person[1:] for person in data]
    frame = pd.DataFrame(data)
    today = datetime.now(timezone.utc) - timedelta(days=1)
    name = ""
    mon = (today - timedelta(days=today.weekday() + 1))
    name += str(mon.year) + "_" + str(mon.month) + "_" + str(mon.day) + "_"
    sun = (today + timedelta(days=7 - today.weekday()))
    name += str(sun.year) + "_" + str(sun.month) + "_" + str(sun.day)
    frame.to_csv(dir_path + "\\files\\" + name + ".csv",sep = ".")


def load(client : discord.Client) -> []:
    dir_path = os.getcwd()

    today = datetime.now(timezone.utc)
    mon = (today - timedelta(days=today.weekday() + 1))
    name = str(mon.year) + "_" + str(mon.month) + "_" + str(mon.day) + "_"
    sun = (today + timedelta(days=7 - today.weekday()))
    name += str(sun.year) + "_" + str(sun.month) + "_" + str(sun.day)
    dict = {}
    for x in range(1,9):
        dict[x] = eval
    if os.path.exists(dir_path + "\\files\\" + name + ".csv"):
        frame = pd.read_csv(dir_path + "\\files\\" + name + ".csv", sep = ".",converters=dict)
    else:
        return []
    guilds = client.guilds
    for guild in guilds:
        if guild.id == 703873995279171584:
            unova = guild
    out = frame.values.tolist()
    out = [[unova.get_member(person[1])]+person[2:] for person in out]
    return out
