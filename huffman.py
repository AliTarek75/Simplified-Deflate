from queue import PriorityQueue
class node:
    def __init__(self,freq,left=None,right=None,element=None):
        self.freq=freq
        self.right=right
        self.left=left 
        self.element=element
    @classmethod
    def merge(cls,n1,n2):
        return cls((n1.freq+n2.freq),n1,n2)

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
def createfreq(list):
    frequency_table={}

    for i in list:
        if i in frequency_table:
            frequency_table[i]+=1
        else:
            frequency_table[i]=1
    frequency_table = dict(sorted(frequency_table.items(), key=lambda item: item[1], reverse=True))

    return frequency_table
def huffman(frequency):
    queue=PriorityQueue()
    for key in frequency:
        n=node(freq=frequency[key],element=key)
        queue.put((n.freq,key,n))
    while queue.qsize()>1:
        n1_freq,s1, n1_node = queue.get()
        n2_freq,s2, n2_node = queue.get()
        merged=node.merge(n1_node,n2_node)
        queue.put((merged.freq,min(s1,s2),merged))
    return queue.get()

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








