import prime_math

decompose_map = {}
LIMIT = 4096


def encode_chr(i):
    return decompose_map[i]


def encode(text):
    return __encode(text).replace('<>', '')


def __encode(text):
    last = 0
    brainfuck = []
    for c in text:
        next_chr = ord(c)
        if next_chr > 127:
            continue
        if next_chr is last:
            brainfuck.insert(-1, '.')
        else:
            brainfuck += encode_chr(next_chr - last) + '.<'
        if len(brainfuck) >= LIMIT:
            return str(brainfuck[:LIMIT])
        last = next_chr
    if len(brainfuck) > 0:
        brainfuck.pop(-1)
    return ''.join(brainfuck)


def largest_divisor(n):
    i = int(n/2)
    while i != 0:
        if n % i == 0:
            return i
        i -= 1
    return 1


def isprime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

def __possible_mults(n):
    res = []
    i = int(n / 2)
    while i != 0:
        if n % i == 0:
            b = int(n/i)
            res.append((i, b))
            if b > 10:
                return res
        i -= 1
    return res

def __decompose(i):
    if i <= 5:
        return 0, i, 1

    if isprime(i):
        off = 1
        i -= 1
    else:
        off = 0

    choices = __possible_mults(i)
    chosen = None
    for choice in choices:
        if not chosen or abs(chosen[0] - chosen[1]) > abs(choice[0] - choice[1]):
            chosen = choice

    return off, chosen[1], chosen[0]


def __smallify(numbs):
    for x in range(0, len(numbs)):
        if x > 5:
            continue
        for y in range(x + 1, len(numbs)):
            if y > 5:
                continue
            r = numbs[x] * numbs[y]
            if r <= 5:
                numbs[x] = r
                del numbs[y]
                numbs.sort(reverse=True)
                __smallify(numbs)
                return


def __build_map():
    decompose_map[0] = '>'
    for i in range(1, 255):
        res = __decompose(i)
        decompose_map[i] = mul_to_brainfuck(res, False)
        decompose_map[-i] = mul_to_brainfuck(res, True)


def mul_to_brainfuck(tup, negative):
    off, a, b = tup
    ch = '-' if negative else '+'
    if a is 1 or b is 1:
        return '>' + (ch * (a*b+off))

    res = ('+' * a) + '[>' + (ch * b) + '<-]>' + (ch * off)
    return res


__build_map()
#print(encode('W JESÙ'))
