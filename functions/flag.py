import asyncio
from datetime import datetime, timedelta, timezone
from threading import Timer
import re
import discord
import random
import functions.saveload as saveload
from discord.ext import commands, tasks

lifetime = []
highscores = []
flagtimes = [12, 19, 21, 22, 23]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
owner = None

async def hourlySave():
    saveload.save(highscores)
    nextHour = datetime.now(timezone.utc)+timedelta(minutes=1,hours=1)
    nextHour = nextHour.replace(second=0,minute=0)
    now = datetime.now(timezone.utc)
    diff = (nextHour-now).total_seconds()
    print(diff)
    saveload.save(highscores)
    await asyncio.sleep(diff)
    task = asyncio.create_task(hourlySave())
    print("saved")
    await task


async def callSundays():
    today = datetime.now(timezone.utc)
    sun = (today + timedelta(days=7 - today.weekday())).replace(hour=0, minute=0, second=0)
    diff = (sun - today).total_seconds()
    print(str(diff))
    print(datetime.now())

    await asyncio.sleep(diff)
    task = asyncio.create_task(weeklyCalc())
    await task

    task = asyncio.create_task(callSundays())
    await task


async def weeklyCalc():
    saveload.save(highscores)
    list = [(x[0], sum([sum(y) for y in x[1:]])) for x in highscores]
    list.sort(key=lambda x: x[1] + random.uniform(0, 1), reverse=True)
    brk = len(list)

    for a in range(0, len(list)):
        if list[a][1] < 100:
            brk = a
            break;
    list = list[0:brk]
    out = discord.Embed(title="Weekly reset", description="Top 3, randomly chosen 1 (Must be over 100 points)",
                        color=0x00ff00)
    top_three = "```Rank  Name                        Points\n"
    for i in range(0, 3):
        if len(list) == 0:
            break
        if list[0][0].nick is None:
            name = str(list[0][0].name + "#" + list[0][0].discriminator)[:26]
        else:
            name = str(list[0][0].nick)[:26]
        top_three = top_three + str(i + 1) + (" " * (5 - (i + 1) // 10)) + name + (" " * (28 - len(name))) + str(
            list[0][1]) + "\n"
        list.pop(0)
    total = 0
    for i in range(0, len(list)):
        total += list[i][1]
    soFar = 0
    if (len(list) > 0):
        val = random.uniform(0, total)
        for i in range(0, len(list)):
            soFar += list[i][1]
            if val <= soFar:
                if list[0][0].nick is None:
                    name = str(list[i][0].name + "#" + list[i][0].discriminator)[:26]
                else:
                    name = str(list[i][0].nick)[:26]
                top_three = top_three + "4" + (" " * (5 - (4) // 10)) + name + (
                        " " * (28 - len(name))) + str(
                    list[i][1])
                break
    top_three += "```"
    out.add_field(name="Top Three", value=top_three)
    await owner.send_results(returnScoreBoard())
    await owner.send_results(out)
    highscores.clear()


def addScore(userName: discord.Member, dirtyScore: str) -> None:
    x = datetime.now(timezone.utc)
    temp = re.findall("\d+", dirtyScore)
    if len(temp) == 0:
        return
    score = int(temp[0])
    addedIn = False
    flagSlot = -1
    for i in range(0, 5):
        if x.hour >= flagtimes[i]:
            flagSlot += 1
    for player in highscores:
        if player[0] == userName:
            if (flagSlot < 0):
                if x.weekday() == 0:
                    return
                player[x.weekday()][-1] = score
            else:
                player[x.weekday() + 1][flagSlot] = score
            addedIn = True
            break
    if not addedIn:
        highscores.append([userName] + [[0 for i in range(0, 5)] for x in range(0, 7)])
        if (flagSlot < 0):
            if x.weekday() == 0:
                return
            highscores[-1][x.weekday()][-1] = score
        else:
            highscores[-1][x.weekday() + 1][flagSlot] = score
    return


def editScore(userName: discord.Member, txt: str, mentions: [discord.member]) -> None:
    if not mentions or userName.guild_permissions.administrator == False:
        return
    x = datetime.now(timezone.utc)
    nums = re.findall("\s\+?-?\d+", txt)
    raceNum = int(nums[0])
    score = int(nums[1])
    found = False
    for player in highscores:
        if player[0] == mentions[0]:
            player[(raceNum) // 5 + 1][raceNum % 5] = score
            found = True
            break
    if not found:
        highscores.append([mentions[0]] + [[0 for i in range(0, 5)] for x in range(0, 7)])
        highscores[-1][(raceNum) // 5 + 1][raceNum % 5] = score
    return


# Individual
# TODO: Add total lifetime
def returnIndividual(userName: discord.Member, mentions: [discord.Member]) -> discord.Embed():
    if (userName is None or userName not in [x[0] for x in highscores]) and (
            len(mentions) == 0 or mentions[0] not in [x[0] for x in highscores]):
        return discord.Embed(title="Unova Flag: " + userName.display_name, description="No races done!")
    if len(mentions) > 0 and mentions[0] in [x[0] for x in highscores]:
        userName = mentions[0]
    today = datetime.now(timezone.utc)
    mon = (today - timedelta(days=today.weekday() + 1))
    sun = (today + timedelta(days=7 - today.weekday()))
    out = discord.Embed(title="Unova Flag: " + userName.display_name,
                        description="Week: " + str(mon.month) + "/" + str(mon.day) + " - " + str(sun.month) + "/" + str(
                            sun.day), color=0x00ff00)
    list = [(x[0], sum([sum(y) for y in x[1:]])) for x in highscores]
    list.sort(key=lambda x: x[1], reverse=True)
    namesOnly = [x[0] for x in list]
    rank = namesOnly.index(userName) + 1
    pointSum = list[rank - 1][1]
    out.add_field(name="Rank", value=str(rank), inline=True)
    numRaces = 0
    list = []
    for player in highscores:
        if player[0] == userName:
            list = player[1:]
            numRaces = sum([sum([1 if race else 0 for race in day]) for day in player[1:]])
    out.add_field(name="Races", value=str(numRaces), inline=True)
    avg = "0"
    if not numRaces == 0:
        avg = str(round(pointSum / numRaces, 2))
    out.add_field(name="Points(Avg)", value=str(pointSum) + "(" + avg + ")", inline=True)

    for day in range(0, 7):
        data = ":sunrise:" + str(list[day][0]) + "\n" + ":sunny:" + str(list[day][1]) + "\n" + ":city_sunset:" + str(
            list[day][2]) + "\n" + ":milky_way:" + str(list[day][3]) + "\n" + ":milky_way:" + str(list[day][4])
        out.add_field(name=weekdays[day], value=data, inline=True)
    return out


# Scoreboard
def returnScoreBoard() -> discord.Embed():
    today = datetime.now(timezone.utc)
    mon = (today - timedelta(days=today.weekday() + 1))
    sun = (today + timedelta(days=7 - today.weekday()))
    out = discord.Embed(title="Unova Gpq Leaderboard",
                        description="Week: " + str(mon.month) + "/" + str(mon.day) + " - " + str(sun.month) + "/" + str(
                            sun.day), color=0x00ff00)
    if not highscores:
        out.add_field(name="Top ten", value="No races done!")
        return out
    list = [(x[0], sum([sum(y) for y in x[1:]])) for x in highscores]
    list.sort(key=lambda x: x[1], reverse=True)
    out.add_field(name="Total", value=sum([sum([sum(y) for y in x[1:]]) for x in highscores]), inline=False)

    topTen = "```Rank  Name                        Points\n"
    for i in range(0, 9):
        if i >= len(list):
            break
        if list[i][0].nick is None:
            name = str(list[i][0].name + "#" + list[i][0].discriminator)[:26]
        else:
            name = str(list[i][0].nick)[:26]
        topTen = topTen + str(i + 1) + (" " * (5 - (i + 1) // 10)) + name + (" " * (28 - len(name))) + str(
            list[i][1]) + "\n"
    topTen += "```"
    out.add_field(name="Top ten", value=topTen)
    return out
