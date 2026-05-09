import math

# Create the header in one long string and combine it with payload from stage3
def createHeader(stage2):
    payload,lit_codes, dist_codes = pipeline(stage2)

    LIT_BW, DIST_BW = calculateBW(lit_codes,dist_codes)
    litBits = litPadding(LIT_BW, lit_codes)
    distBits = distPadding(DIST_BW, dist_codes)

    # Header format: [4 bits LIT_BW][4 bits DIST_BW][286 × LIT_BW bits LIT_TABLE][30 × DIST_BW bits DIST_TABLE]
    headerStr = format(LIT_BW, '04b') + format(DIST_BW, '04b') + litBits + distBits

    # Pad header size to be multiple of 8 so file size is an integer number of bytes
    while ((len(headerStr) % 8) != 0):
        headerStr += '0'
    
    headerBytes = bytearray()
    for i in range(0, len(headerStr), 8):
        headerBytes.append(int(headerStr[i:i+8], 2))
    
    # Final output is bytearray contain header + payload 
    return headerBytes + payload

# Calculate minimum number of bits needed to represent maximum length/distance codes in binary
def calculateBW(lit_codes,dist_codes):
    # Find maximum code length from literal/distance dictionary
    max_length = max(length for code,length in lit_codes.values())
    max_distance = max(length for code,length in dist_codes.values())

    LIT_BW = 0
    DIST_BW = 0

    # Calculate the number of bits required by the following formula: ⌊log2(M)⌋ + 1
    if (max_length > 0):
        LIT_BW = math.floor(math.log2(max_length))+1

    if (max_distance > 0):
        DIST_BW = math.floor(math.log2(max_distance))+1

    return LIT_BW, DIST_BW


# Pad 286 literal/length symbol if it exists otherwise symbol is 0, because all symbols must be written in the header for easy decoding
# Value of keys in lit_codes dictionary is a tuple (code, length) so we pad index 1 in tuples
def litPadding(LIT_BW,lit_codes):
    litBits = ""

    if (LIT_BW > 0):
        for i in range(286):
            if (i in lit_codes):
                litBits += format(lit_codes[i][1], f'0{LIT_BW}b')
            else:
                litBits += format(0, f'0{LIT_BW}b')

    return litBits

# Pad 30 distance symbol if it exists otherwise symbol is 0, because all symbols must be in the header for easy decoding
# value of keys in dist_codes dictionary is a tuple (code, length) so we pad index 1 in tuples
def distPadding(DIST_BW, dist_codes):
    distBits = ""

    if (DIST_BW > 0):
        for i in range(30):
            if (i in dist_codes):
                distBits += format(dist_codes[i][1], f'0{DIST_BW}b')
            else:
                distBits += format(0, f'0{DIST_BW}b')

    return distBits