# Base values for each length symbol
LENGTH_BASE = [
    3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31,
    35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258
]

# Number of extra bits to read for each length symbol
LENGTH_EXTRA = [
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
    3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0
]

# Base values for each distance symbol
DISTANCE_BASE = [
    1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193,
    257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145,
    8193, 12289, 16385, 24577
]

# Number of extra bits to read for each distance symbol
DISTANCE_EXTRA = [
    0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6,
    7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13
]

def generate_event_stream(tokens):
    output = []

    for token in tokens:
        if isinstance(token, tuple):
            length = token[0]
            distance = token[1]
            temp = []

            # Length Processing by going backwards
            # This avoids the off by one and going out of bounds issues
            i = len(LENGTH_BASE) - 1
            while length < LENGTH_BASE[i]:
                i -= 1

            temp.append(257+i)
            num = length - LENGTH_BASE[i]
            extra = LENGTH_EXTRA[i]

            # append the correct string and an empty string if extra bit length is 0
            binary_str = format(num, f'0{extra}b') if extra != 0 else ""
            temp.append(binary_str)
        
            # Distance Processing by going backwards
            i = len(DISTANCE_BASE) - 1
            while distance < DISTANCE_BASE[i]:
                i -= 1

            temp.append(i)
            num = distance - DISTANCE_BASE[i]
            extra = DISTANCE_EXTRA[i]

            # append the correct string and an empty string if extra bit length is 0
            binary_str = format(num, f'0{extra}b') if extra != 0 else ""
            temp.append(binary_str)

            output.append(tuple(temp))
                
        else:
            output.append(token)

    # End Event
    output.append(256)

    return output
