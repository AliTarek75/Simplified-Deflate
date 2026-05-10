from queue import PriorityQueue

# Tree node class
class node:
    def __init__(self,freq,left=None,right=None,element=None):
        self.freq=freq
        self.right=right
        self.left=left 
        self.element=element

    #returns a merged node
    @classmethod
    def merge(cls,n1,n2):
        return cls((n1.freq+n2.freq),n1,n2)
    
# Splits the 2nd stage output to two lists of distance symbols and lit/len symbols for easier processing later
# returns both the lists
def convert(stage2_output):
    lit_symbols = []
    dist_symbols = []

    for token in stage2_output:
        # If token is a tuple then it's a match
        if type(token) is tuple:
            len_sym, len_extra, dist_sym, dist_extra = token
            lit_symbols.append(len_sym)
            dist_symbols.append(dist_sym)
        else:
            lit_symbols.append(token)  
    
    return lit_symbols, dist_symbols

# create and outputs a dictionary containing every symbol as key and frequency as value
def createfreq(list):
    frequency_table={}

    for i in list:
        if i in frequency_table:
            frequency_table[i]+=1
        else:
            frequency_table[i]=1

    return frequency_table

# takes the frequency dictionary and outputs the root node of the huffman tree
def huffman(frequency):

    # Handle the single symbol edge case, because this will skip the queue and give the symbol 0 length
    if len(frequency) == 1:
        symbol = list(frequency.keys())[0]

        # Create a root node that points to the symbol node, This ensures the symbol has a length of 1
        return node(freq=frequency[symbol], left=node(freq=frequency[symbol], element=symbol))
    
    queue = PriorityQueue()
    for key in frequency:

        n = node(freq=frequency[key], element=key)
        # Inserts based on frequency as key and symbol in case of a tie
        queue.put((n.freq, key, n))

    while queue.qsize() > 1:
        # Pops 2 nodes merges them then puts them back in again
        n1_freq, s1, n1_node = queue.get()
        n2_freq, s2, n2_node = queue.get()
        merged = node.merge(n1_node, n2_node)
        queue.put((merged.freq, min(s1,s2), merged))
        
    return queue.get()[2]

# takes the root of a tree and returns a dictionary int(symbol) -> int(length)
def get_lengths(node, depth=0, lengths=None):
    if lengths is None:
        lengths={}
    if node.element is not None: 
        lengths[node.element] = depth
    else:
        if node.left:
            get_lengths(node.left, depth+1, lengths)
        if node.right:
            get_lengths(node.right, depth+1, lengths)
    return lengths

# Takes the lenghts dictionary and returns a dictionary int(symbol) -> (int(code), int(length))
# its mostly copy pasted from the pdf with very few modifications
def canonical_codes(lengths):
    # Find the max depth of the tree
    max_bits = max(lengths.values()) if lengths else 0
    
    # Initialize arrays to fit the actual max depth
    count = [0] * (max_bits + 1)
    for length in lengths.values():
        count[length] += 1
    count[0] = 0 

    next_code = [0] * (max_bits + 1)
    code = 0

    for bits in range(1, max_bits + 1):
        code = (code + count[bits - 1]) << 1
        next_code[bits] = code

    symbol_code = {}

    for symbol in sorted(lengths.keys()):
        length = lengths[symbol]
        if length != 0:
            symbol_code[symbol] = (next_code[length], length)
            next_code[length] += 1

    return symbol_code

# the main function applying all of the pipeline 
# returns the payload and the output of the canoniccal codes function for both lit/len and dist respecctively
# the input is stage 2 output
def pipeline(stage2):

    # Initilization steps
    lit,dist = convert(stage2)
    
    lit_tree = huffman(createfreq(lit))
    lit_codes = canonical_codes(get_lengths(lit_tree))

    if dist:
        dist_tree = huffman(createfreq(dist))
        dist_codes = canonical_codes(get_lengths(dist_tree))
    else:
        dist_codes = {}

    # Payload generation
    bits = []
    for token in stage2:
        # If token is a tuple then it's a match
        if type(token) is tuple:
            len_sym, len_extra, dist_sym, dist_extra = token
            code, length = lit_codes[len_sym]

            # format is used to create the actual prefix-free code from its value and length
            bits.append(format(code, f'0{length}b'))

            bits.append(len_extra)

            code, length = dist_codes[dist_sym]
            bits.append(format(code, f'0{length}b'))

            bits.append(dist_extra)
        
        else:
            code, length = lit_codes[token]
            bits.append(format(code, f'0{length}b'))

    bitstream = ''.join(bits)

    # Zero padding for last byte
    remainder = len(bitstream) % 8
    if remainder != 0:
        bitstream += '0' * (8 - remainder)

    # Convertion to bytes
    payload = bytearray()
    for i in range(0, len(bitstream), 8):
        payload.append(int(bitstream[i:i+8], 2))
    
    return payload,lit_codes,dist_codes