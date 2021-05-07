import sys

input = []
timezones = []
neg = {}
pos = {}
for line in sys.stdin:
    input.append(line.rstrip())

for x in range(0,len(input)):
    if(input[x].find("Date:") != -1 ):
        timezones.append(input[x][-5:])

for x in range(0,len(timezones)):
    if(timezones[x] not in neg and timezones[x] not in pos):
        if(int(timezones[x])<0):
            neg[timezones[x]] = 1
        else:
            pos[timezones[x]] = 1
    else:
        if(int(timezones[x])<0):
            neg[timezones[x]] = neg[timezones[x]]+1
        else:
            pos[timezones[x]] = pos[timezones[x]]+1

neg1 = sorted(neg.items(), reverse=True)
pos1 = sorted(pos.items())

for key, value in neg1:
    print(key,value)

for key, value in pos1:
    print(key,value)
