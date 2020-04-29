import os

# print(os.listdir('..'))
dires = []
for (root,dirs,files) in os.walk('..',topdown=True):
    dires.append(dirs)

print(dires)
    # print(root)
    # print('-------------------Dirs')
    # print(dirs)
    # print(files)
