# Maximum distance we can look for a match
WINDOW_SIZE = 32768

MIN_MATCH = 3
MAX_MATCH = 258

# Maximum number of candidates we can check 
MAX_CANDIDATES = 64

# tokenProducer is made to search for a pattern and return list of tokens where literals are int and matches are tuple (length, distance)
def tokenProducer(data):
    tokens = []
    # dictionary to append all the 3 bytes sequences in the input so we can return back faster at specific position and check the match
    table = {}
    i = 0

    while(i < len(data)):
        # If fewer than 3 bytes remain so no match is possible
        if ((len(data) - i) < 3):
            tokens.append(data[i])
            i+=1
            continue

        # Get next 3 bytes together to check if there is a match or no
        current = data[i:i+3]
        if (current in table):
            length = 0
            distance = 0
            # We check the last 64 position where the current match happened to calculate the longest length
            # If lengths are equal take nearest position that's why we reversed the last 64 position to start from newest
            for pos in reversed(table[current][-MAX_CANDIDATES:]):
                matchIdx = i
                matchPos = pos

                # Ignore the match if it's distance is larger than max distance
                if ((i - pos) > WINDOW_SIZE):
                    continue
                # Search for the end of the match and update length
                while(((matchIdx - i) < MAX_MATCH) and (matchIdx < len(data)) and (data[matchPos] == data[matchIdx])):
                    matchPos+=1
                    matchIdx+=1

                if (length < (matchIdx - i)):
                    length = matchIdx - i
                    distance = i - pos
            
            # If match is valid then append it in the table and update all other sequences and jump for the next unchecked byte 
            if (length >= MIN_MATCH):
                tokens.append((length,distance))

                for x in range(i, i+length):
                    if ((x + 3) <= len(data)):
                        table.setdefault(data[x:x+3], []).append(x)
                i += length
            # If match is less than min_match then append literal
            else:
                table.setdefault(current, []).append(i)
                tokens.append(data[i])
                i+=1

        else:
            table.setdefault(current, []).append(i)
            tokens.append(data[i])
            i+=1

    return tokens