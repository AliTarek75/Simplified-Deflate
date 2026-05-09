# max distance we can look for a match
WINDOW_SIZE = 32768

MIN_MATCH = 3
MAX_MATCH = 258

# max number of candidates we can check 
MAX_CANDIDATES = 64

# tokenProducer is made to search for pattern and return list of tokens where literals are int and matches are tuple (length, distance)
def tokenProducer(data):
    tokens = []
    # dict to append all the 3 bytes sequences in the input so we can return back faster at specific pos and check the match
    table = {}
    i = 0

    while(i < len(data)):
        # if fewer than 3 bytes remain so no match is possible
        if ((len(data) - i) < 3):
            tokens.append(data[i])
            i+=1
            continue

        # get next 3 bytes together to check if there is a match or no
        current = data[i:i+3]
        if (current in table):
            length = 0
            distance = 0
            # we check the last 64 position where the current match happened to calculate the longest length
            # if lengths are equal take nearest pos that's why we reversed the last 64 pos to start from newest
            for pos in reversed(table[current][-MAX_CANDIDATES:]):
                matchIdx = i
                matchPos = pos

                # ignore the match if it's distance is larger than max distance
                if ((i - pos) > WINDOW_SIZE):
                    continue
                # search for the end of the match and update length
                while(((matchIdx - i) < MAX_MATCH) and (matchIdx < len(data)) and (data[matchPos] == data[matchIdx])):
                    matchPos+=1
                    matchIdx+=1

                if (length < (matchIdx - i)):
                    length = matchIdx - i
                    distance = i - pos
            
            # if match is valid then append it in the table and update all other sequences and jump for the next byte outside the match
            if (length >= MIN_MATCH):
                tokens.append((length,distance))

                for x in range(i, i+length):
                    if ((x + 3) <= len(data)):
                        table.setdefault(data[x:x+3], []).append(x)
                i += length
            #if match is less than min_match then append literal
            else:
                tokens.append(data[i])
                i+=1

        else:
            table[current] = [i]
            tokens.append(data[i])
            i+=1

    return tokens