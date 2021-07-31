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


def addScore(userName: discord.member, dirtyScore: str) -> None:
    x = datetime.today()
    temp = re.search("\d+", dirtyScore)
    score = int(dirtyScore[temp.start():temp.end()])
    addedIn = False
    for player in highscores:
        if player[0] == userName:
            player[x.weekday()+1] += score
            addedIn = True
            break
    if not addedIn:
        highscores.append([userName, 0, 0, 0, 0, 0, 0, 0])
        highscores[-1][x.weekday()+1] = score
    return


def returnScores() -> [str]:
    out = []
    for member in highscores:
        out.append((member[0].display_name + "#" + member[0].discriminator, sum(member[1:7])))
    return out

def returnScores2() -> discord.Embed():
    today = datetime.today()
    mon = (today - timedelta(days=today.weekday()+1))
    sun = (today + timedelta(days=7-today.weekday()))
    out = discord.Embed(title="Unova Gpq Leaderboard", description="Week: "+str(mon.month)+"/"+str(mon.day)+" - "+str(sun.month)+"/"+str(sun.day), color=0x00ff00)
    out.add_field(name="Ranking", value="Ranking", inline=True)
    out.add_field(name="Field2", value="hi2", inline=True)
    out.add_field(name="Field3", value="hi3", inline=True)
    out.add_field(name="Field4", value="hi4", inline=True)
    return out