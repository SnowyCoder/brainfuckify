import prime_math

decompose_map = {}
LIMIT = 4096


def encode_chr(i):
    return decompose_map[i]


def encode(text):
    computed = __encode(text)
    if len(computed) > 0:
        computed.pop(-1)
    return ''.join(computed).replace('<>', '')


def __encode(text):
    last = 0
    brainfuck = []
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
            next = encode_chr(next_chr - last) + '.<'
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
    # ASCII are espected to be encoded in one byte. a Lookup table is faster and cheaper
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


# deconstructs the given value into a*b+c
def __decompose(i):
    if i <= 5:
        return 1, i, 0

    if is_prime(i):
        off = 1
        i -= 1
    else:
        off = 0

    choices = __possible_mults(i)
    chosen = None
    for choice in choices:
        if not chosen or abs(chosen[0] - chosen[1]) > abs(choice[0] - choice[1]):
            chosen = choice

    return chosen[1], chosen[0], off


# Fills the buffer map used to get the brainfuck source given the value difference
def __build_map():
    decompose_map[0] = ''
    for i in range(1, 255):
        res = __decompose(i)
        decompose_map[i] = mul_to_brainfuck(res, False)
        decompose_map[-i] = mul_to_brainfuck(res, True)


# Transforms the a*b+c form into a[>b<]c brainfuck code, negating it if possible
def mul_to_brainfuck(tup, negative):
    a, b, off = tup
    ch = '-' if negative else '+'
    if a is 1 or b is 1:
        return '>' + (ch * (a * b + off))

    res = ('+' * a) + '[>' + (ch * b) + '<-]>' + (ch * off)
    return res


__build_map()
#print(encode('W la figa'))
