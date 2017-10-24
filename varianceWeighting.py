from math import sqrt

rating = []
cosinearr = []
v = []



#Calculating cosine for 2 users
def cosine(list1,list2,list3):
    n = list1.__len__()
    pairsum = sqrsum1 = sqrsum2 = 0
    for i in list1:
        sqrsum1 += (i*i)
    for i in list2:
        sqrsum2 += (i*i)
    for i in  range (list1.__len__()):
        pairsum += (list1[i]*list2[i]*v[list3[i]])
    denom = sqrt(sqrsum1)*sqrt(sqrsum2)
    if denom == 0:
        return 0
    else:
        return pairsum/denom



#Start of the code
f = open("Variance_weight/um.out","w")

global rating
global pearsonarr
global v
meanitem = []
variance = []
minvar = 1000000000000000000000
maxvar = 0


#Creating the rating list
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


#Calculating mean rating for item
meanitem.append(0)
for j in range(1,3953):
    user = 0
    total = 0
    for i in range(6041):
        if rating[i][j] != 0:
            total += rating[i][j]
            user += 1
    if user == 0:
        meanitem.append(0)
    else:
        meanitem.append(total/user)


#Calculating variance
variance.append(0)
for j in range(1,3953):
    count = 0
    numer = 0
    for i in range(6041):
        if rating[i][j] != 0:
            count += 1
            temp = (rating[i][j]-meanitem[j])
            temp = temp * temp
            numer += temp
    if count >= 2:
        variance.append(numer/(count-1))
    else:
        variance.append(0)
    minvar = min(minvar, variance[j])
    maxvar = max(maxvar, variance[j])


#Calculating the list V
v.append(0)
for j in range(1,3953):
    numer = variance[j] - minvar
    denom = maxvar
    if denom != 0:
        v.append(float(numer)/float(denom))
    else:
        v.append(0)

# Creating cosine matrix
for i in range(6041):
    nl = []
    for j in range(6041):
        nl.append(0)
    cosinearr.append(nl)

# Calculating cosine matrix
for i in range(1, 6041):
    for j in range(1, 6041):
        if cosinearr[i][j] == 0 and i != j:
            a1 = a2 = a3 = []
            for k in range(3953):
                if rating[i][k] != 0 and rating[j][k] != 0:
                    a1.append(rating[i][k])
                    a2.append(rating[j][k])
                    a3.append(k)
            cosinearr[i][j] = cosinearr[j][i] = cosine(a1, a2, a3)


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
            ratingpred += (rating[i][itemid]*cosinearr[i][uid])
            simsum += cosinearr[i][uid]
    if simsum != 0:
        ratingpred /= simsum
    else:
        ratingpred = 0
    errorlist.append(abs(ratingpred-trating))
    f.write(str(uid)+"\t"+str(itemid)+"\t"+str(ratingpred)+"\n")
f.write("MAE "+str(sum(errorlist)/errorlist.__len__())+"\n")
f.write("NMAE "+str(sum(errorlist)/(4*errorlist.__len__()))+"\n")
f.close()