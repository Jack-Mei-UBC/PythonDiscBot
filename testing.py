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
# import pandas as pd
# import os
# from datetime import datetime, timedelta
#
# def startWeekly():
#     x = datetime.today()
#     y = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes = 1)
#
# if __name__ == '__main__':
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     files = "/files/"
#     directory = dir_path + files
#     test = []
#     test.append(["p0"] + [[i for i in range(0, 5)] for x in range(0, 7)])
#     test.append(["p1"] + [[i for i in range(0, 5)] for x in range(0, 7)])
#     frame = pd.DataFrame(test)
#     frame.to_csv(directory + "/test.csv")
if __name__ == '__main__':
    while(True):
        print("yes")