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
    import asyncio
    import time


    async def hello():
        print('Hello ...')
        time.sleep(5)
        print('... World!')


    async def main():
        await asyncio.gather(hello(), hello())


    asyncio.run(main())
