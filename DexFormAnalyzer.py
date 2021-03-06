__author__ = 'Rorschach'

class DexAnalyzer:
    className = ""
    def __init__(self):
        self.className = "Dex analyzer"

class DexHeaderProperty:
    stringIdxSize = 0
    stringIdxOff = 0
    typeIdxSize = 0
    typeIdxOff = 0
    methodIdsSize = 0
    methodIdsOff = 0
    classDefSize = 0
    classDefOff = 0

    def __init__(self,dexContent):
        self.classDefSize = self.readDexHeaderProperty(dexContent,0x60,4)
        self.classDefOff = self.readDexHeaderProperty(dexContent,0x64,4)
        print "--Mess-- read class def size and off is 0x%08X and 0x%08X" %(self.classDefSize,self.classDefOff)

        self.stringIdxSize = self.readDexHeaderProperty(dexContent,0x38,4)
        self.stringIdxOff = self.readDexHeaderProperty(dexContent,0x3C,4)
        print "--Mess-- read string idx size and off is 0x%08X and 0x%08X" %(self.stringIdxSize,self.stringIdxOff)

        self.typeIdxSize = self.readDexHeaderProperty(dexContent,0x40,4)
        self.typeIdxOff = self.readDexHeaderProperty(dexContent,0x44,4)
        print "--Mess-- read type idx size and off is 0x%08X and 0x%08X" %(self.typeIdxSize,self.typeIdxOff)

        self.methodIdsSize = self.readDexHeaderProperty(dexContent,0x58,4)
        self.methodIdsOff = self.readDexHeaderProperty(dexContent,0x5c,4)
        print "--Mess-- read method idx size and off is 0x%08X and 0x%08X" %(self.methodIdsSize,self.methodIdsOff)

    def readDexHeaderProperty(self,dexContent,start,length):
        list1 = []
        for hexword in range(start,start+length):
            tmp = ord(dexContent[hexword])
            list1.append(tmp)

        number = endianToNormal(list1[0:4],4)
        return number

class DexClassDataHeader:
    staticFieldsSize = 0
    instanceFieldsSize = 0
    directMethodsSize = 0
    virtualMethodsSize = 0
    headerTakeBits = 0

    def __init__(self,dexContent,offset):
        analyStr = []
        analyStr = analyzeleb128(dexContent,offset + self.headerTakeBits)
        self.staticFieldsSize = analyStr[1]
        self.headerTakeBits += analyStr[0]
        analyStr = []
        analyStr = analyzeleb128(dexContent,offset + self.headerTakeBits)
        self.instanceFieldsSize = analyStr[1]
        self.headerTakeBits += analyStr[0]
        analyStr = []
        analyStr = analyzeleb128(dexContent,offset + self.headerTakeBits)
        self.directMethodsSize = analyStr[1]
        self.headerTakeBits += analyStr[0]
        analyStr = []
        analyStr = analyzeleb128(dexContent,offset + self.headerTakeBits)
        self.virtualMethodsSize = analyStr[1]
        self.headerTakeBits += analyStr[0]

class DexCode:
    registersSize = 0
    insSize = 0
    outsSize = 0
    triesSize = 0
    debugInfoOff = 0
    insnsSize = 0
    insns = []

    def __init__(self,offset,dexContent):
        self.registersSize = endianToNormal(stringListToIntList(dexContent[offset:offset+2],2),2)
        offset += 2
        self.insSize       = endianToNormal(stringListToIntList(dexContent[offset:offset+2],2),2)
        offset += 2
        self.outsSize      = endianToNormal(stringListToIntList(dexContent[offset:offset+2],2),2)
        offset += 2
        self.triesSize     = endianToNormal(stringListToIntList(dexContent[offset:offset+2],2),2)
        offset += 2
        self.debugInfoOff  = endianToNormal(stringListToIntList(dexContent[offset:offset+4],4),4)
        offset += 4
        self.insnsSize     = endianToNormal(stringListToIntList(dexContent[offset:offset+4],4),4)
        offset += 4
        insnsSize = self.insnsSize * 2
        self.insns = []

        while insnsSize != 0:
            insnsSize -= 1
            tmp = ord(dexContent[offset])
            offset += 1
            self.insns.append(tmp)

def endianToNormal(byteArray,length):
    s = 0
    s1 = 1
    for letter in range(0,length):
        s += byteArray[letter] * s1
        s1 *= 0x100
    return s

def stringListToIntList(stringList,length):
    intList =[]
    for i in range(0,length):
        intList.append(ord(stringList[i]))
    return intList

def analyzeleb128(dexContent,offset):
    listNumberAndValue = [1,0] # first means value take number of bits, second means value
    if ord(dexContent[offset]) > 0x7f:
        listNumberAndValue[0] += 1
        listNumberAndValue[1] = ord(dexContent[offset]) & 0x7f

        if ord(dexContent[offset+1]) > 0x7f:
            listNumberAndValue[0] += 1
            listNumberAndValue[1] = (listNumberAndValue[1] & 0x7f)|((ord(dexContent[offset+1]) & 0x7f)<<7)

            if ord(dexContent[offset+2]) > 0x7f:
                listNumberAndValue[0] += 1
                listNumberAndValue[1] |= ((ord(dexContent[offset+2]) & 0x7f)<<14)
                if ord(dexContent[offset+3]) > 0x7f:
                    listNumberAndValue[0] += 1
                    listNumberAndValue[1] |= ((ord(dexContent[offset+3]) & 0x7f)<<21)
                    listNumberAndValue[1] |= ((ord(dexContent[offset+4]) & 0x7f)<<28)
                else:
                    listNumberAndValue[1] |= ((ord(dexContent[offset+3]) & 0x7f)<<21)
            else:
                listNumberAndValue[1] |= ((ord(dexContent[offset+2]) & 0x7f)<<14)
        else:
            listNumberAndValue[1] = (listNumberAndValue[1] & 0x7f)|((ord(dexContent[offset+1]) & 0x7f)<<7)
    else:
        listNumberAndValue[1] = ord(dexContent[offset])
    return listNumberAndValue