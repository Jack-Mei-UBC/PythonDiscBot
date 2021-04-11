import pickle
save = "data.pkl"
banList = []
with open (save, 'rb') as input:
    banList = pickle.load(input)
print(banList)

with open(save, 'wb') as output:
    pickle.dump(banList,output,pickle.HIGHEST_PROTOCOL)
print(banList)