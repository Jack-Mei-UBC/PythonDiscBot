# import pickle
# save = "data.pkl"
# banList = []
# with open (save, 'rb') as input:
#     banList = pickle.load(input)
# print(banList)
#
# with open(save, 'wb') as output:
#     pickle.dump(banList,output,pickle.HIGHEST_PROTOCOL)
# print(banList)
import pandas as pd
import os
from datetime import datetime, timedelta

def startWeekly():
    x = datetime.today()
    y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes = 1)

if __name__ == '__main__':
    import functions.saveload as saveload

    test = []
    test.append(["p0"] + [[i for i in range(0, 5)] for x in range(0, 7)])
    test.append(["p1"] + [[i for i in range(0, 5)] for x in range(0, 7)])
    saveload.save(test)
