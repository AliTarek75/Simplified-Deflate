from huffman import canonical_codes 
from event_generator import LENGTH_BASE, LENGTH_EXTRA, DISTANCE_BASE, DISTANCE_EXTRA 

# The data variable in any function here is assumed to takes a single string of bits
# Any other form will not work

# Interprets the integer between start and end in the bit string
def read_int(data, start, end):
    return int(data[start : end], 2)

# Finds a valid code from the code list (keys) from start in the bit string
# Returns both the key and the length
def decode_symbol(data, start, keys):
    for i in range(1, 17):
        key = data[start : start+i]
        if key in keys:
            return key, i

# Calculates the huffman cannonical codes but inverts the order of the dict
# Original dict was int(symbol) -> (int(code), int(length))
# Invert is string(final calculated code) -> int(symbol) 
def canonical_invert(lengths):
    codes = canonical_codes(lengths)
    result = {}
    for symbol, (code, length) in codes.items():
        result[format(code, f'0{length}b')] = symbol

    return result
