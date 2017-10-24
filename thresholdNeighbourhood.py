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


def getNhood(uid,itemId):
    neighbour = []
    for i in range(6041):
        if i!=uid and rating[i][itemId]!=0:
            temp = (signif[uid][i],i)
            neighbour.append(temp)
    neighbour.sort(key=itemgetter(0),reverse=True)
    return neighbour


def getRating(uid,itemId,threshold):
    ratingpred = simsum = 0
    neighbour = getNhood(uid,itemId)
    i = 0
    while True:
        if i==len(neighbour) or signif[uid][neighbour[i][1]]<threshold:
            break
        if rating[neighbour[i][1]][itemId] != 0:
            ratingpred += (neighbour[i][0] * (rating[neighbour[i][1]][itemId] - meanRating[neighbour[i][1]]))
            simsum += neighbour[i][0]
        i += 1
    if simsum != 0:
        rate = ratingpred / simsum
        rate += meanRating[uid]
    else:
        rate = meanRating[uid]
    return rate


f = open("Threshold/um.out","w")

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



#Creating cosine matrix
for i in range(6041):
    nl = []
    for j in range(6041):
        nl.append(0)
    signif.append(nl)


#Calculating cosine matrix
for i in range(1,6041):
    for j in range(1,6041):
        if signif[i][j] == 0 and i != j:
            a1=a2=[]
            for k in range(1,3953):
                if rating[i][k] != 0 and rating[j][k] != 0:
                    a1.append(rating[i][k])
                    a2.append(rating[j][k])
            if a1.__len__()>0 and a2.__len__()>0:
                tempcos = cosine(a1,a2)
                signif[i][j] = signif[j][i] = tempcos


#Getting dataset
lines = [line.rstrip('\n') for line in open('TestData/um.test')]

i = 0.4
while i<=1.2:
    errorlist = []
    for item in lines:
        temp=item.split('\t')
        uid = int(temp[0])
        itemid = int(temp[1])
        trating = int(temp[2])
        ratingpred = getRating(uid,itemid,i)

        errorlist.append(abs(ratingpred-trating))
    f.write(str(sum(errorlist)/(4*errorlist.__len__()))+"\n")
    i += 0.05
f.close()