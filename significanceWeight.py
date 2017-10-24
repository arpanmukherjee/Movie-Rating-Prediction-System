from math import sqrt
from operator import itemgetter

rating = []
signif = []
meanRating = []


def corritem(u1,u2):
    ans = 0
    for i in range(3953):
        if rating[u1][i] != 0 and rating[u2][i] != 0:
            ans += 1
    return ans

def cosine(list1,list2):
    n = list1.__len__()
    pairsum = sqrsum1 = sqrsum2 = 0
    for i in list1:
        sqrsum1 += (i*i)
    for i in list2:
        sqrsum2 += (i*i)
    for i in  range (list1.__len__()):
        pairsum += (list1[i]*list2[i])
    denom = sqrt(sqrsum1)*sqrt(sqrsum2)
    if denom == 0:
        return 0
    else:
        return pairsum/denom


def getNhood(uid):
    neighbour = []
    for i in range(6041):
        if i==uid:
            continue
        temp = (signif[uid][i],i)
        neighbour.append(temp)
    neighbour.sort(key=itemgetter(0),reverse=True)
    return neighbour


def getRating(uid,itemId):
    ratingpred = simsum = 0
    neighbour = getNhood(uid)
    i = cnt = 0
    while True:
        if i==50 or i==len(neighbour):
            break
        if rating[neighbour[i][1]][itemId] != 0:
            ratingpred += (signif[uid][neighbour[i][1]] * (rating[neighbour[i][1]][itemId] - meanRating[neighbour[i][1]]))
            simsum += signif[uid][neighbour[i][1]]
            cnt += 1
        i += 1
    if simsum != 0:
        rate = ratingpred / simsum
        rate += meanRating[uid]
    else:
        rate = 0
    return rate


f = open("User_Significance/um.out","w")

lines = [line.rstrip('\n') for line in open('TestData/um.base')]
global rating
global signif
global meanRating
for i in range(6041):
    nl = []
    for j in range(3953):
        nl.append(0)
    rating.append(nl)
    meanRating.append(0)

#Storing data in the matrix
for item in lines:
    temp = item.split('\t')
    rating[int(temp[0])][int(temp[1])]=int(temp[2])


for i in range(6041):
    cnt = ans = 0
    for j in range(3953):
        if rating[i][j]!=0:
            ans += rating[i][j]
            cnt += 1
    if cnt != 0:
        meanRating[i] = float(ans)/float(cnt)



#Creating pearson matrix
for i in range(6041):
    nl = []
    for j in range(6041):
        nl.append(0)
    signif.append(nl)

for wt in range(5,51,5):
    for i in range(1,6041):
        for j in range(1,6041):
            signif[i][j]=0

    for i in range(1,6041):
        for j in range(1,6041):
            if signif[i][j] == 0 and i != j:
                a1=a2=[]
                for k in range(1,3953):
                    if rating[i][k] != 0 and rating[j][k] != 0:
                        a1.append(rating[i][k])
                        a2.append(rating[j][k])
                tempcos = cosine(a1,a2)
                ans = min(corritem(i,j),wt)/wt
                ans = ans * tempcos
                signif[i][j] = signif[j][i] = ans



    #Getting dataset
    lines = [line.rstrip('\n') for line in open('TestData/um.test')]
    errorlist = []
    for item in lines:
        temp=item.split('\t')
        uid = int(temp[0])
        itemid = int(temp[1])
        trating = int(temp[2])
        ratingpred = int(round(getRating(uid,itemid)))
        errorlist.append(abs(ratingpred-trating))
    f.write(str(float(sum(errorlist))/float(4*errorlist.__len__()))+"\n")
f.close()
