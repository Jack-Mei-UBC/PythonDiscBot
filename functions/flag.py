import os
from datetime import datetime, timedelta
from threading import Timer
import re
import discord
lifetime = []
highscores = []
flagtimes = [12, 19, 21, 22, 23]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dir_path = os.path.dirname(os.path.realpath(__file__))
files = "/files/"
directory = dir_path + files

def startWeekly():
    x = datetime.today()
    y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=(7 - x.weekday()))
    delta_t = y - x

    secs = delta_t.total_seconds()

    t = Timer(secs, weeklyCalc)
    t.start()


def weeklyCalc():
    startWeekly()
    highscores = []



def addScore(userName: discord.Member, dirtyScore: str) -> None:
    x = datetime.today()
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
    x = datetime.today()
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
def returnIndividual(userName: discord.Member) -> discord.Embed():
    if userName is None or userName not in [x[0] for x in highscores]:
        return
    today = datetime.today()
    mon = (today - timedelta(days=today.weekday() + 1))
    sun = (today + timedelta(days=7 - today.weekday()))
    out = discord.Embed(title="Unova Flag: " + userName.display_name,
                        description="Week: " + str(mon.month) + "/" + str(mon.day) + " - " + str(sun.month) + "/" + str(sun.day), color=0x00ff00)
    list = [(x[0], sum([sum(y) for y in x[1:]])) for x in highscores]
    list.sort(key=lambda x: x[1], reverse=True)
    namesOnly = [x[0] for x in list]
    rank = namesOnly.index(userName)+1
    pointSum = list[rank-1][1]
    out.add_field(name="Rank", value=str(rank), inline=True)
    numRaces = 0
    list = []
    for player in highscores:
        if player[0] == userName:
            list = player[1:]
            numRaces = sum([sum([1 if race else 0 for race in day]) for day in player[1:]])
    out.add_field(name="Races", value=str(numRaces), inline=True)
    out.add_field(name="Point(Avg)", value=str(pointSum)+"("+str(round(pointSum/numRaces,2))+")", inline=True)

    for day in range(0,7):
        data = ":sunrise:" + str(list[day][0])+"\n"+":sunny:" + str(list[day][1]) + "\n" +":city_sunset:" + str(list[day][2]) + "\n" +":milky_way:" + str(list[day][3]) + "\n" + ":milky_way:" + str(list[day][4])
        out.add_field(name=weekdays[day], value=data,inline=True)
    return out


# Scoreboard
def returnScoreBoard() -> discord.Embed():
    today = datetime.today()
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
