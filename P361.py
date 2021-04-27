getNegation = lambda digit: "1" if digit == "0" else "0"
getSubBitsEven = lambda bits: bits[::2]
getSubBitsOdd = lambda bits: getNegation(bits[0]) + bits[1::2]

def getStartFlags(bits):
    startEven = startOdd = True
    for i in range(1, len(bits), 2):
        if bits[i] == bits[i - 1]:
            startEven = False
            break
    for i in range(2, len(bits), 2):
        if bits[i] == bits[i - 1]:
            startOdd = False
            break
    return startEven, startOdd

def isLegal(bits):
    if len(bits) <= 2: return True
    startEven, startOdd = getStartFlags(bits)
    result = False
    if startEven: result = result or isLegal(getSubBitsEven(bits))
    if startOdd:  result = result or isLegal(getSubBitsOdd(bits))
    return result

zipParas = {}
def getZipParas(zipNumber, mod):
    if mod not in zipParas: zipParas[mod] = [[2 % mod], [[0, 1 % mod]]]
    zipBases, zipDigitValues = zipParas[mod]
    while zipNumber >= len(zipBases):
        zipDigitValues.append([*map(lambda v: (v + 1) * (zipBases[-1] - 1) % mod, zipDigitValues[-1])])
        zipBases.append((zipBases[-1] ** 2) % mod)
    return zipBases[zipNumber], zipDigitValues[zipNumber]

def getValue(bits, mod, zipNumber):
    result = 0
    zipBase, zipDigitValue = getZipParas(zipNumber, mod)
    for digit in bits:
        result = (result * zipBase + zipDigitValue[int(digit)]) % mod
    return result

cacheCount = {}
def getCount(starts, remainLength):
    if not isLegal(starts): return 0
    if remainLength == 0:   return 1
    key = starts + " " + str(remainLength)
    if key not in cacheCount:
        startEven, startOdd = getStartFlags(starts)
        if startEven and startOdd:
            cacheCount[key] = getCount(starts + "0", remainLength - 1) + getCount(starts + "1", remainLength - 1)
        elif startEven:
            if len(starts) % 2 == 0: remainLength += 1
            cacheCount[key] = getCount(getSubBitsEven(starts), remainLength // 2)
        elif startOdd:
            if len(starts) % 2 == 1: remainLength += 1
            cacheCount[key] = getCount(getSubBitsOdd(starts), remainLength // 2)
    return cacheCount[key]

def getNthValue(starts, remainLength, n, mod, zipNumber=0):
    if not isLegal(starts): raise RuntimeError
    if remainLength == 0:
        if n == 1: return getValue(starts, mod, zipNumber), getValue(starts[:-1], mod, zipNumber), starts[-1]
        else: raise RuntimeError
    startEven, startOdd = getStartFlags(starts)
    if startEven and startOdd:
        count = getCount(starts + "0", remainLength - 1)
        if n <= count: return getNthValue(starts + "0", remainLength - 1, n, mod, zipNumber)
        else:          return getNthValue(starts + "1", remainLength - 1, n - count, mod, zipNumber)
    exceptedLength = len(starts) + remainLength
    zipBase, zipDigitValue = getZipParas(zipNumber, mod)
    if startEven:
        if len(starts) % 2 == 0: remainLength += 1
        result, withoutLastDigitResult, lastDigit = getNthValue(getSubBitsEven(starts), remainLength // 2, n, mod, zipNumber + 1)
        tmpResult = (withoutLastDigitResult * zipBase + zipDigitValue[int(lastDigit)]) % mod
        if exceptedLength % 2 == 0: withoutLastDigitResult, lastDigit = tmpResult, getNegation(lastDigit)
        else: result = tmpResult
    if startOdd:
        if len(starts) % 2 == 1: remainLength += 1
        result, withoutLastDigitResult, lastDigit = getNthValue(getSubBitsOdd(starts), remainLength // 2, n, mod, zipNumber + 1)
        tmpLength, tmpDigit = (len(starts) // 2 + remainLength // 2) * 2, zipDigitValue[int(getNegation(starts[0]))]
        result = (result - tmpDigit * pow(zipBase, tmpLength + 1, mod)) % mod
        withoutLastDigitResult = (withoutLastDigitResult - tmpDigit * pow(zipBase, tmpLength - 1, mod)) % mod
        tmpResult = (withoutLastDigitResult * zipBase + zipDigitValue[int(lastDigit)]) % mod
        if exceptedLength % 2 == 0: result = tmpResult
        else: withoutLastDigitResult, lastDigit = tmpResult, getNegation(lastDigit)
    return result, withoutLastDigitResult, lastDigit

def getBitLength(lo, hi, function, goal):
    while hi - lo != 1:
        mi = (lo + hi) // 2
        if function(mi) >= goal: hi = mi
        else: lo = mi
    return hi

def getAnValue(n, mod):
    k, count, kTotal, kRemain = 1, 6, 11, 3
    while count + kTotal < n:
        k, count, kTotal, kRemain = k + 1, count + kTotal, kTotal * 4 - kRemain, kRemain * 2
    tmp = kRemain // 3
    if tmp + (tmp * 2) ** 2 + count < n:
        count += tmp + (tmp * 2) ** 2
        lo, hi, function = 3 * tmp + 1, 4 * tmp + 1, lambda x: ((7 * tmp + x) * (x - 1 - 3 * tmp)) // 2
    else:
        lo, hi, function = 2 * tmp + 1, 3 * tmp + 1, lambda x: (tmp + x) * (x - 1 - tmp * 2)
    bitLength = getBitLength(lo, hi, function, n - count)
    count += function(bitLength - 1)
    return getNthValue("1", bitLength - 1, n - count, mod)[0]

def getAnswer(k=18, mod=10 ** 9):
    result = 0
    for i in range(1, k + 1):
        result = (result + getAnValue(10 ** i, mod)) % mod
    return result

print(getAnswer())