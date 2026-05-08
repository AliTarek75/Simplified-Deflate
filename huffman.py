from queue import PriorityQueue
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
# splits the 2nd stage output to distance symbols and lit/len symbols
def convert(stage2_output):
    lit_symbols = []
    dist_symbols = []

    for token in stage2_output:
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
    # sorts with respect to values(its actually unneeded bec the priority queue handles it)
    frequency_table = dict(sorted(frequency_table.items(), key=lambda item: item[1], reverse=True))

    return frequency_table

# takes the frequency dictionary and outputs the root of the huffman tree
def huffman(frequency):
    queue=PriorityQueue()
    for key in frequency:

        n=node(freq=frequency[key],element=key)
        # inserts based on frequency as key and symbol in case of a tie
        queue.put((n.freq,key,n))
    while queue.qsize()>1:
        #pops 2 nodes merges them then puts them back in again
        n1_freq,s1, n1_node = queue.get()
        n2_freq,s2, n2_node = queue.get()
        merged=node.merge(n1_node,n2_node)
        queue.put((merged.freq,min(s1,s2),merged))
    return queue.get()
# takes the root of a tree and outputs a  dictionary containing each symbol as key and its code lenght as value
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
"""takes the lenghts dictionary and outputs a dictionary containing the symbol as key and a 
 tuple containing its code and code lenght lenght respectiveely as value(its mostly copy pasted from the pdf with very few modifications)"""
def canonical_codes(lengths):
 
    count = [0] * 16
    for length in lengths.values():
        count[length] += 1
    count[0] = 0 

    next_code = [0] * 16
    code = 0

    for bits in range(1, 16):
        code = (code + count[bits - 1]) << 1
        next_code[bits] = code

    symbol_code = {}

    for symbol in sorted(lengths.keys()):
        length = lengths[symbol]
        if length != 0:
            symbol_code[symbol] = (next_code[length], length)
            next_code[length] += 1

    return symbol_code
# the main function applying all of the pipeline returning the payload and the output of the canoniccal codes function for both lit/len and dist respecctively
#the input is stage 2 output
def pipeline(stage2):
    lit,dist = convert(stage2)
    lit_freq=createfreq(lit)
    dist_freq=createfreq(dist)
    lit_tree=huffman(lit_freq)
    dist_tree=huffman(dist_freq)
    lit_len=get_lengths(lit_tree)
    dist_len=get_lengths(dist_tree)
    lit_codes=canonical_codes(lit_len)
    dist_codes=canonical_codes(dist_len)
    #payload generation
    bits = []
    for token in stage2:
        if type(token) is tuple:
            len_sym, len_extra, dist_sym, dist_extra = token
            code, length = lit_codes[len_sym]
            # format is to to limit the code to its length
            bits.append(format(code, f'0{length}b'))

            if len_extra:
                bits.append(len_extra)

            code, length = dist_codes[dist_sym]
            bits.append(format(code, f'0{length}b'))

            if dist_extra:
                bits.append(dist_extra)
        
        else:
            code, length = lit_codes[token]
            bits.append(format(code, f'0{length}b'))

    bitstream = ''.join(bits)
    #zero padding for lastbyte
    remainder = len(bitstream) % 8
    if remainder != 0:
        bitstream += '0' * (8 - remainder)
    # convert to bytes
    payload = bytearray()
    for i in range(0, len(bitstream), 8):
        payload.append(int(bitstream[i:i+8], 2))
    
    return payload,lit_codes,dist_codes







