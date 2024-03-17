a = [1,2,1,3,5,6,4]
max = 0
maxIndex = 0
for index,i in enumerate(a) :
    if i > max :
        max = i
        maxIndex = index
print(maxIndex)