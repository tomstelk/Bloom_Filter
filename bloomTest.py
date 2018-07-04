import bloomStruc
import numpy as np
from collections import Counter
from scipy.stats import chisquare



#Test 1: Bloom data structure correctly queries all data stored in data structure
print('Test 1: Bloom data structure correctly queries all data stored in data structure')

t1SetSize=1000
t1TestStrs= [str(i) for i in range(0,t1SetSize)]
b=bloomStruc.bloomStruc(t1TestStrs,blmTargetFPR=0.001)
posTest= []
for t in t1TestStrs:
    posTest.append(b.bloomQuery(t))

print(all(posTest))




#Test 2: Bloom data structure has correct FPR for various target FPRs
print()
print()
print('Test 2: Bloom data structure has correct FPR for various FPRs')

t2InDataSize = 1000
t2TestSetSize = 100000
t2TestStrs= [str(i) for i in range(0,t2InDataSize)]
#Create lots of strings outside data already stored
t2TestInput = [str(t2InDataSize+i) for i in range(0,t2TestSetSize)]

fprSet = [0.0000001, 0.0001, 0.001, 0.1, 0.25, 0.5, 0.9, 0.99] 


for fpr in fprSet:
    fprTestRes = []
    b=bloomStruc.bloomStruc(t2TestStrs,blmTargetFPR=fpr)
    for t in t2TestInput:
        fprTestRes.append(b.bloomQuery(t))
    
    fprRatio = fprTestRes.count(True)/t2TestSetSize

    print('Actual fpr on test set: ' + str(fprRatio) + ', theoretical fpr: ' + str(b.getTheoFPR()), ', target fpr: ' + str(fpr) )




#Test 3: Test bloom hash function uniformly maps random input strings to {0, ..., m-1}
print()
print()
print('Test bloom hash function uniformly maps random input strings to {0, ..., m-1}')
t3blmM = 20
t3blmK = 1
t3SetSize = 100000
b=bloomStruc.bloomStruc(inStrList=[''],blmM=t3blmM, blmK=t3blmK)
testStrs = [str(i) for i in np.random.rand(t3SetSize)]
t3_uniTestRes = []
for t in testStrs:
    t3_uniTestRes.append(b.bloomMultiHash(t)[0])
    

    
t3_c=Counter(t3_uniTestRes)
print('Bloom hash should map each member of test set to one of {0, ..., ' + str(t3blmM-1) + '} with uniform freq: ' + str(t3SetSize/t3blmM))

for mVal in range(0,t3blmM):
    print('Index ' + str(mVal) + ': ' + str( t3_c[mVal]))
    
t3X2Test = chisquare(list(t3_c.values()),t3SetSize/t3blmM)
print('Test 3 chi-Square p-val: ' + str( t3X2Test[1]))



#Test 4: Test bloom hash functions uniformly map an input strings to {0, ..., m-1}
print()
print()
print('Test 4: Test bloom hash functions uniformly map an input string to {0, ..., m-1}')
t4blmM = 20
t4blmK = 1
t4SetSize = 100000
t4TestString = ''
b=bloomStruc.bloomStruc(inStrList=[''],blmM=t4blmM, blmK=t4blmK)

testHashSeeds = range(0,t4SetSize)
t4_uniTestRes = []

for t in testHashSeeds:
    t4_uniTestRes.append(b.bloomHash(t4TestString,t))
    

    
t4_c=Counter(t4_uniTestRes)
print('Bloom hash should map each member of test set to one of {0, ..., ' + str(t4blmM-1) + '} with uniform freq: ' + str(t4SetSize/t4blmM))

for mVal in range(0,t4blmM):
    print('Index ' + str(mVal) + ': ' + str( t4_c[mVal]))
    
t4X2Test = chisquare(list(t4_c.values()),t4SetSize/t4blmM)
print('Test 4 chi-Square p-val: ' + str( t4X2Test[1]))

#Test 5: FPR increases as add more data
print()
print()
print('Test 5: FPR increases as add more data')
t5InitSetSize=1000
t5TargetFPR = 0.001
t5TestStrs= [str(i) for i in range(0,t5InitSetSize)]
b=bloomStruc.bloomStruc(t5TestStrs,blmTargetFPR=0.001)
t5NumTests = 10
t5TestSize = 100000
t5TestStrs = [str(i) for i in range(-t5TestSize,-1)]
t5Res = []

for t in range(0,t5NumTests):
    moreData = [str(i) for i in range(t5InitSetSize*(t+1),t5InitSetSize*(t+2))]
    b.addData(moreData)


for t in t5TestStrs:
    t5Res.append(b.bloomQuery(t))

t5ActualFPR = t5Res.count(True)/t5TestSize
print('Actual fpr on test set: ' + str(t5ActualFPR) + ', theoretical fpr: ' + str(b.getTheoFPR()), ', original target fpr: ' + str(t5TargetFPR) )
