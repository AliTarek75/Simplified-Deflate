WINDOW_SIZE = 32768
MIN_MATCH = 3
MAX_MATCH = 258
MAX_CANDIDATES = 64

data = open('data.txt', 'rb').read()

def tokenProducer(data):
    tokens = []
    table = {}
    i = 0

    while(i < len(data)):
        if ((len(data) - i) < 3):
            tokens.append(data[i])
            i+=1
            continue

        current = data[i:i+3]
        if (current in table):
            length = 0
            final_pos = 0
            for pos in reversed(table[current][-MAX_CANDIDATES:]):
                matchIdx = i
                matchPos = pos

                if ((i - pos) > WINDOW_SIZE):
                    continue

                while(((matchIdx - i) < MAX_MATCH) and (matchIdx < len(data)) and (data[matchPos] == data[matchIdx])):
                    matchPos+=1
                    matchIdx+=1

                if (length < (matchIdx - i)):
                    length = matchIdx - i
                    final_pos = i - pos
            
            if (length >= MIN_MATCH):
                tokens.append((length,final_pos))

                for x in range(i, i+length):
                    if ((x + 3) <= len(data)):
                        table.setdefault(data[x:x+3], []).append(x)
                i += length

            else:
                tokens.append(data[i])
                i+=1

        else:
            table[current] = [i]
            tokens.append(data[i])
            i+=1
    return tokens