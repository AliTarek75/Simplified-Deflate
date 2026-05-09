import math

def compressFile(stage2):
    payload,lit_codes, dist_codes = pipeline(stage2)

    LIT_BW, DIST_BW = calculateBW(lit_codes,dist_codes)
    litBits = litPadding(LIT_BW, lit_codes)
    distBits = distPadding(DIST_BW, dist_codes)

    headerStr = format(LIT_BW, '04b') + format(DIST_BW, '04b') + litBits + distBits
    while ((len(headerStr) % 8) != 0):
        headerStr += '0'
    
    headerBytes = bytearray()
    for i in range(0, len(headerStr), 8):
        headerBytes.append(int(headerStr[i:i+8], 2))
    
    file = open("test.bin", 'wb')
    file.write(headerBytes + payload)


def calculateBW(lit_codes,dist_codes):
    max_length = 0
    for value in lit_codes.values():
        if (value[1] > max_length):
            max_length = value[1]

    max_distance = 0
    for value in dist_codes.values():
        if (value[1] > max_distance):
            max_distance = value[1]

    LIT_BW = 0
    DIST_BW = 0
    if (max_length > 0):
        LIT_BW = math.floor(math.log2(max_length))+1
    if (max_distance > 0):
        DIST_BW = math.floor(math.log2(max_distance))+1
    return LIT_BW, DIST_BW


def litPadding(LIT_BW,lit_codes):
    litBits = ""

    if (LIT_BW > 0):
        for i in range(286):
            if (i in lit_codes):
                litBits += format(lit_codes[i][1], f'0{LIT_BW}b')
            else:
                litBits += format(0, f'0{LIT_BW}b')

    return litBits

def distPadding(DIST_BW, dist_codes):
    distBits = ""

    if (DIST_BW > 0):
        for i in range(30):
            if (i in dist_codes):
                distBits += format(dist_codes[i][1], f'0{DIST_BW}b')
            else:
                distBits += format(0, f'0{DIST_BW}b')

    return distBits