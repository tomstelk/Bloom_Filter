import pymmh3
import numpy as np
import datetime 


class bloomStruc:
    def __init__(self, inStrList=[], blmM=-1, blmK=-1, blmExN = -1, blmTargetFPR = 0.01):
        
        assert isinstance(inStrList, list), "If input data is provided, must be in list"
        assert blmExN!=-1 or not not inStrList, "Input dataset or expected size of dataset must be given"
        assert blmTargetFPR>0 and blmTargetFPR<1, "Target FPR rate must be a valid probability"
        
        print(str(datetime.datetime.now().time()) + ': Creating Bloom data structure ... ')
        
        self._dataSetSize = 0
        self._targetFPR = blmTargetFPR
        #If expected size of dataset is given, use it, else estimate expected size of dataset given data provided
        if blmExN == -1:
            self._blmExN = len(inStrList)
        else: 
            self._blmExN = blmExN
        
        #If bloom parameter M is given, use it, else calculate using target false-positive rate
        if blmM==-1:
            self._blmM= int(np.rint(abs((self._blmExN * np.log(blmTargetFPR)) / (np.log(2) ** 2))))
        else:
            self._blmM = blmM
        
        print('Bloom parameter M assigned value: ' + str(self._blmM))
        
        #If bloom parameter k is given, use it, else set as optimal k given the value of bloom parameter blmM, 
        #and the expected size of the data
            
        if blmK==-1:
            self._blmK = max(1,int(np.rint(self._blmM*np.log(2)/self._blmExN)))
        else:
            self._blmK=blmK
            
        print('Bloom parameter K assigned value: ' + str(self._blmK))
        
        
        self._blmFilter = np.full(self._blmM, False, dtype=bool)
        self.addData(inStrList)
        
        
              
        
        
    def __select(self, lst, indices):
        return (lst[i] for i in indices) 
    
    def bloomHash(self,inStr, hashSeed):
        #Use 32-bit hash function pymmh3 to map a string to an integer in {0, ..., m-1}
        
        maxHash = 2**31-1
        h=pymmh3.hash(inStr,hashSeed)/maxHash
        return int(0.5*self._blmM*(h+1))
    
    
    
    def bloomMultiHash(self,inStr):
        #Use different seed numbers to generate multiple hash functions
        
        return [self.bloomHash(inStr, i) for i in range(0,self._blmK)]
    
  
    def __bloomAdd(self, inStr):
        #Add inStr to bloom index by mapping in str to a logical array and adding to 
        #current bloom filter
        
        blIndx = self.bloomMultiHash(inStr)
        for i in blIndx:
            self._blmFilter[i] = True
            
    def addData(self, inStrList):
        #Add inStrList to data structure by mapping each inStr to a logical array and adding to 
        #current bloom filter
        assert isinstance(inStrList, list), "Input data must be in a list"
        print(str(datetime.datetime.now().time()) + ': Adding data ...')
        
        for i  in range(0,len(inStrList)):
            self.__bloomAdd(inStrList[i])
        
        print(str(datetime.datetime.now().time()) + ': Adding data complete')
        self._dataSetSize =self._dataSetSize +len(inStrList)
        self._theoFPR = (1-np.exp(-self._blmK*self._dataSetSize/self._blmM))**self._blmK
        
        print('Theoretical FPR based on current dataset size: ' + str(self._theoFPR) + ', target FPR: ' + str(self._targetFPR) )
    
    def bloomQuery(self, inStr):
        #Query if inStr is in structure - if return False then inStr has been added,
        #if returns True then inStr mightve been added
        blIndx = self.bloomMultiHash(inStr)
        return all(list(self.__select(self._blmFilter,blIndx)))
    
    def getTheoFPR(self):
        return self._theoFPR

    def getTargetFPR(self):
        return self._targetFPR


