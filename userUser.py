from math import sqrt

rating = []
pearsonarr = []


#Calculating pearson for 2 users
def pearson(list1,list2):
    n = list1.__len__()
    sum1 = sum(list1)
    sum2 = sum(list2)
    pairsum = sqrsum1 = sqrsum2 = 0
    for i in list1:
        sqrsum1 += (i*i)
    for i in list2:
        sqrsum2 += (i*i)
    for i,j in zip(list1,list2):
        pairsum += (i*j)
    numer = (pairsum*n) - (sum1*sum2)
    denom = sqrt(((n*sqrsum1)-(sum1*sum1))*((n*sqrsum2)-(sum2*sum2)))
    if denom == 0:
        return 0
    else:
        return numer/denom



#Start of the code
f = open("User_user/um.out","w")

global rating
global pearsonarr
for i in range(6041):
    nl = []
    for j in range(3953):
        nl.append(0)
    rating.append(nl)

#Storing data in the matrix
lines1 = [line.rstrip('\n') for line in open('TestData/um.base')]
for item in lines1:
    temp = item.split('\t')
    rating[int(temp[0])][int(temp[1])]=int(temp[2])


#Creating pearson matrix
for i in range(6041):
    nl = []
    for j in range(6041):
        nl.append(0)
    pearsonarr.append(nl)


#Calculating pearson matrix
for i in range(1,6041):
    for j in range(1,6041):
        if pearsonarr[i][j] == 0 and i != j:
            a1=a2=[]
            for k in range(3953):
                if rating[i][k] != 0 and rating[j][k] != 0:
                    a1.append(rating[i][k])
                    a2.append(rating[j][k])
            pearsonarr[i][j]=pearsonarr[j][i]=pearson(a1,a2)


#Getting dataset
lines = [line.rstrip('\n') for line in open('TestData/um.test')]
errorlist = []
for item in lines:
    temp=item.split('\t')
    uid = int(temp[0])
    itemid = int(temp[1])
    trating = int(temp[2])

    ratingpred = 0
    simsum = 0
    for i in range(6041):
        if i != uid and rating[i][itemid] != 0:
            ratingpred += (rating[i][itemid]*pearsonarr[i][uid])
            simsum += pearsonarr[i][uid]
    if simsum != 0:
        ratingpred /= simsum
    else:
        ratingpred = 0
    errorlist.append(abs(ratingpred-trating))
    f.write(str(uid)+"\t"+str(itemid)+"\t"+str(ratingpred)+"\n")
f.write("MAE "+str(sum(errorlist)/errorlist.__len__())+"\n")
f.write("NMAE "+str(sum(errorlist)/(4*errorlist.__len__()))+"\n")
f.close()