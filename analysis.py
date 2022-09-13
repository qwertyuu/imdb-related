import json

with open("movielist.txt", "r") as fp:
    original_list = fp.read().split("\n")

with open("relateds.json", "r") as sauce:
    relateds = json.load(sauce)

#print([elem[1] for elem in relateds])
only_relateds = [elem[1] for elem in relateds]
flat_list = [item for sublist in only_relateds for item in sublist]
print(json.dumps(list(set(flat_list) - set(original_list))))
