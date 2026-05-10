from huffman import canonical_codes 
from event_generator import LENGTH_BASE, LENGTH_EXTRA, DISTANCE_BASE, DISTANCE_EXTRA 

# The data variable in any function here is assumed to takes a single string of bits
# Any other form will not work

# interpret the integer between start and end in the bit string
def read_int(data, start, end):
    return int(data[start : end], 2)

# find valid code from the code list (keys) from start in the bit string
# returns both the key and the length
def decode_symbol(data, start, keys):
    for i in range(1, 300):
        key = data[start : start+i]
        if key in keys:
            return key, i
        
    raise ValueError(f"No valid Huffman code found at index {start}.")

# calculates the huffman cannonical codes but inverts the order of the dict
# original dict was int(symbol) -> (int(code), int(length))
# invert is string(final calculated code) -> int(symbol) 
def canonical_invert(lengths):
    codes = canonical_codes(lengths)
    result = {}
    for symbol, (code, length) in codes.items():
        result[format(code, f'0{length}b')] = symbol

    return result

# The decompresser function, uses a main index (idx) 
# that gets updated throughout the function to read the bit string (data)
def decompress(data):
    idx = 0

    # 1. Reading the header

    # Reads the Bit widths for both literals and distances
    LIT_BW = read_int(data, idx, idx+4)
    idx += 4
    DIST_BW = read_int(data, idx, idx+4)
    idx += 4

    lit_len = []
    dist_len = []

    # Reads the huffman lengths from the next two tables
    for _ in range(286):
        length = read_int(data, idx, idx + LIT_BW)
        lit_len.append(length)
        idx += LIT_BW  

    for _ in range(30):
        length = read_int(data, idx, idx + DIST_BW)
        dist_len.append(length)
        idx += DIST_BW

    # Calculates the cannonical codes
    lit_codes = canonical_invert(dict(enumerate(lit_len)))
    dist_codes = canonical_invert(dict(enumerate(dist_len)))

    # This will hold the final decompressed result 
    result = bytearray()
    
    # Skip the rest of the header extra padding
    if idx % 8 != 0:
        idx += (8 - idx % 8)

    # 2. Reading the payload
    while True:

        # Decodes a literal event symbol
        lit_key, i = decode_symbol(data, idx, lit_codes)
        literal = lit_codes[lit_key]

        idx += i

        # If literal is >256 it's a match, if <256 it's a normal literal 
        # other than that we reached the end and we break
        if literal > 256:

            # calculates the length of the extra bits (0, 1, 2...) 
            # then slices the data to get the exact bit string for the extra bits
            extra_length = LENGTH_EXTRA[literal-257]
            extra = data[idx : idx+extra_length]

            # calculates the actual length for the match
            # we get the starting point then add the extra bits if it's not an empty string 
            # doing int() on an empty string gives an error
            length = LENGTH_BASE[literal-257] + (int(extra, 2) if extra else 0)

            idx += extra_length

            # Decodes a distance event symbol 
            dist_key, i = decode_symbol(data, idx, dist_codes)
            dist_value = dist_codes[dist_key]

            idx += i

            # Calculates the actual distance for the match
            extra_length = DISTANCE_EXTRA[dist_value]
            extra = data[idx : idx+extra_length]
            distance = DISTANCE_BASE[dist_value] + (int(extra, 2) if extra else 0)
        
            idx += extra_length
            
            # Decodes the match from length and distance that we calculated
            # We keep copying from distance away and append length times
            for _ in range(length):
                result.append(result[-distance])

        elif literal < 256:
            result.append(literal)
        else:
            break

    return result