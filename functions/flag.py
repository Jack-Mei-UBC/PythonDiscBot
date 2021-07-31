from datetime import datetime, timedelta
from threading import Timer
import re
import discord

highscores = []


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
    temp = re.search("\d+", dirtyScore)
    score = int(dirtyScore[temp.start():temp.end()])
    addedIn = False
    for player in highscores:
        if player[0] == userName:
            player[x.weekday() + 1] += score
            addedIn = True
            break
    if not addedIn:
        highscores.append([userName, 0, 0, 0, 0, 0, 0, 0])
        highscores[-1][x.weekday() + 1] = score
    return


def editScore(userName: discord.Member, dirtyScore: str, mentions: [discord.member]) -> None:
    if not mentions or userName.guild_permissions.administrator == False:
        return
    x = datetime.today()
    temp = re.search("-?\d+", dirtyScore)
    score = int(dirtyScore[temp.start():temp.end()])
    for player in highscores:
        if player[0] == mentions[0]:
            player[x.weekday() + 1] += score
            break
    return


# Individual
# TODO: Add total lifetime
def returnIndividual() -> [str]:
    out = []
    for member in highscores:
        out.append((member[0].display_name + "#" + member[0].discriminator, sum(member[1:7])))
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
    list = [(x[0], sum(x[1:])) for x in highscores]
    list.sort(key=lambda x: x[1], reverse=True)
    out.add_field(name="Total", value=sum([sum(x[1:]) for x in highscores]), inline=False)

    topTen = "```Rank  Name                        Points\n"
    for i in range(0, 9):
        if i >= len(list):
            break
        name = str(list[i][0].nick)[:26]
        topTen = topTen + str(i + 1) + (" " * (5 - (i + 1) // 10)) + name + (" " * (28 - len(name))) + str(
            list[i][1]) + "\n"
    topTen += "```"
    out.add_field(name="Top ten", value=topTen)
    return out
