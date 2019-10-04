decompose_map = {}
LIMIT = 4096


def encode_chr(i):
    return decompose_map[i]


def encode(text):
    computed = __encode(text)
    computed = ''.join(computed).replace('><', '')  # Remove '><'
    computed_m = __encode_M(text)
    #print(len(computed))
    #print(len(computed_m))
    return computed if len(computed)<len(computed_m) else computed_m # return best of two algorithms

def __encode_M_bitset(text,last,v): # try M encoding using bits in v
	res = ">+"
	for j in range(0,len(v)): # for every bit
		if j!=0: # if not first bit, move the new power of to from position 0 to position 1
			res+="<[->+<]>"
		res+="[-" # iterate with position 1 (power of 2 corresponding to v[j]th bit)
		if j!=len(v)-1: # if not last bit, generate next power of two in position 0
			res+="<"
			res+="+"*(1<<(v[j+1]-v[j]))
			res+=">"
		l=0 # calculate last character in text you have to go to
		for i in range(v[j],8 if j==len(v)-1 else v[j+1]):
			l=max(l,last[i])
		for i in range (0,l+1): # for every character <=l, add the correct powers of two
			res+=">"
			for k in range(v[j],8 if j==len(v)-1 else v[j+1]):
				if ord(text[i])&(1<<k)!=0:
					res+="+"*(1<<(k-v[j]))
		res+="<"*(l+1) # go back to the beginning
		res+="]" # and loop
	res+=">[.>]" # print result
	return res

def __encode_M(text):
	res=""
	tmp=""
	last = [-1,-1,-1,-1,-1,-1,-1,-1]
	for i in range(0,len(text)):
		for j in range(0,8): # calculate last character in text that needs the jth bit
			if ord(text[i])&(1<<j) != 0:
				last[j]=i
	for bs in range(1,128,2): # for every possible bitset
		v=[]
		for j in range(0,8): # convert the bitset into a vector
			if bs&(1<<j)!=0:
				v.append(j)
		tmp=__encode_M_bitset(text,last,v) # try encoding
		if res=="" or len(res)>len(tmp):   # and keep if it is better
			res=tmp
	return res

def __encode(text):
    # 2 channels used: index and chars
    last = 0
    brainfuck = ['>']
    for c in text:
        next_chr = ord(c)
        if next_chr > 127:
            continue
        # If the next char is the same as the last one
        if next_chr is last:
            # First check if there's no more space
            if len(brainfuck) >= LIMIT:
                return brainfuck
            # Then add a print instruction between the last . and the < char
            brainfuck.insert(-1, '.')
        else:
            # Compute how much text the next char would take
            next = encode_chr(next_chr - last) + '.'
            # And check if there's space to add it
            if len(brainfuck) + len(next) > LIMIT:
                # If there's no space left return the string up to the last char
                return brainfuck
            # Add the text to the buffer
            brainfuck += next
            # Update the value
            last = next_chr
    return brainfuck


def is_prime(n):
    """Returns True if n is prime."""
    # ASCII are expected to be encoded in one byte. a Lookup table is faster and cheaper
    return n in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]


# Returns all the possible multipliers that have the second value lesser than 10
def __possible_mults(n):
    res = []
    i = int(n / 2)
    while i != 0:
        if n % i == 0:
            b = int(n / i)
            res.append((i, b))
            if b > 10:
                return res
        i -= 1
    return res


def __decompose(i, find_alt=True):
    # There are tree forms:
    # 0 -> n                        Length: n
    # 1 -> <a[>b<-]> (a*b=n)        Length: 7 + a + b
    # 2 -> <a[>b<-]>c (a*b+c=n)     Length: 7 + a + b + c
    if i <= 10:
        return 1, i, 0

    # Find best couple:
    best_a, best_b = 128, 128  # It can't be larger than sqrt(127)
    for a, b in __possible_mults(i):
        if a + b < best_a + best_b:
            best_a, best_b = a, b

    # Test if the best couple beats the 0 form
    if i <= 7 + best_a + best_b:
        best_a, best_b = 1, i
        offset = 0
    else:
        offset = 7

    if not find_alt:
        return best_a, best_b, 0

    best_c = 0

    # Search alternative from neighbours
    for x in range(i - 5, i + 6):
        if x == i:
            continue
        alt_a, alt_b, _ = __decompose(x, False)
        c = i - x

        if alt_a + alt_b + abs(c) + 7 < best_a + best_b + abs(best_c) + offset:
            # If the alternative is found then swap it with the
            best_a, best_b = alt_a, alt_b
            best_c = c

    return best_a, best_b, best_c


# Fills the buffer map used to get the brainfuck source given the value difference
def __build_map():
    decompose_map[0] = ''
    for i in range(1, 255):
        res = __decompose(i)
        assert res[0] * res[1] + res[2] == i
        decompose_map[i] = mul_to_brainfuck(res, False)
        decompose_map[-i] = mul_to_brainfuck(res, True)


# Transforms the a*b+c form into a[>b<-]>c< brainfuck code, negating it if possible
def mul_to_brainfuck(tup, negative):
    a, b, off = tup
    bch = '-' if negative else '+'
    if negative:
        off = -off
    if a is 1 or b is 1:
        return bch * (a * b + off)

    offch = '-' if off < 0 else '+'
    res = '<' + ('+' * a) + '[>' + (bch * b) + '<-]>' + (offch * abs(off))
    #print("{} = ({} * {} + {}) -> {}".format((a * b * (-1 if negative else 1) + off), a, -b if negative else b, off, res))
    return res

__build_map()
print(decompose_map)
print(encode('Hello world!'))
#print(encode('this string is very long, so probabilly encoded_m algorithm is better'))