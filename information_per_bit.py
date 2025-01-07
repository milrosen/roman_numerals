import math

base_letters = ['M', 'D', 'C', 'L', 'X', 'V', 'I']

def base_ten_to_roman(num):
    base_numbers = [1000, 500, 100, 50, 10, 5, 1]

    out = ''
    for (l, v) in zip(base_letters, base_numbers):
        out += l * (num // v)
        num %= v
    return out

def combine(n1, n2):
    if not n1: return n2
    if not n2: return n1

    l1, c1 = n1
    l2, c2 = n2
    return (l1 + l2, c1 + c2)

def pop_min(q1, q2):
    if not q1 and not q2: return None

    if not q1:
        return q2.pop(0)
    if not q2:
        return q1.pop(0)
    
    c1 = q1[0][1]
    c2 = q2[0][1]

    if c1 < c2:
        return q1.pop(0)
    return q2.pop(0)

def gen_huffman_tree():
    symbol_counts = {"M":0, "D":0, "C":0, "L":0, "X":0, "V": 0, "I":0}
    for i in range(2, 4001):
        r = base_ten_to_roman(i)
        for s in r: symbol_counts[s] += 1
    
    q1 = list(symbol_counts.items())

    q1.sort(key=lambda x: x[1])
    q2 = []
    tree = {}
    root = ''
    while q1 or q2:
        n1 = pop_min(q1, q2)
        if not q1 and not q2: break
        n2 = pop_min(q1, q2)

        combined = combine(n1, n2)
        tree[combined[0]] = [n1[0], n2[0]]
        root = combined[0]
        q2.append(combined)
    
    return tree, root

def encode_roman(tree, root, roman):
    out = ''
    for s in roman:
        cur = root
        while len(cur) != 1:
            l, r = tree[cur]
            if s in l:
                cur = l
                out += "0"
            else:
                cur = r
                out += '1'
    return out

tree, root = gen_huffman_tree()
print(tree)
r = base_ten_to_roman(75)
print(r)
print(encode_roman(tree, root, r))
avg_log_factor = 0

avg_inf = 0
for i in range(2, 4001):
    r = base_ten_to_roman(i)
    # code = encode_roman(tree, root, r)
    # information = math.log2(i) / len(code)
    # information = (len(r) * 2.5) / math.log2(i)
    # avg_inf += information
    x = math.exp(math.log(i)/len(r))
    avg_log_factor += x
print(avg_log_factor / 4001)