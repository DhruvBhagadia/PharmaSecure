import math
from . import primes

def invmod(a, p, maxiter=1000000):
    """The multiplicitive inverse of a in the integers modulo p:
         a * b == 1 mod p
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def modpow(base, exponent, modulus):
    """Modular exponent:
         c = b ^ e mod m
       Returns c.
       (http://www.programmish.com/?p=34)"""
    result = 1
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

class PrivateKey(object):

    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invmod(self.l, n)
        #self.a = str(self.l)+" "+ str(self.m)

    def get_list(self):
        return [self.l,self.m]


class PublicKey(object):

    @classmethod
    def from_n(cls, n):
        return cls(n)

    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1


    def __repr__(self):
        return  str(self.n)

def generate_keypair(bits):
    p = primes.generate_prime(bits / 2)
    q = primes.generate_prime(bits / 2)
    #print(p,q)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

def encrypt(pub, plain):
    while True:
        r = primes.generate_prime(int(round(math.log(pub, 2))))
        if r > 0 and r < pub:
            break
    pub_n_sq = pub*pub
    pub_g= pub+1
    x = pow(r, pub, pub_n_sq)
    cipher = (pow(pub_g, plain, pub_n_sq) * x) % pub_n_sq
    return cipher

def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    pub_n_sq = pub*pub
    return a * b % pub_n_sq

def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * modpow(pub.g, n, pub.n_sq) % pub.n_sq

def e_mul_const(pub, a, n):
    """Multiplies an ancrypted integer by a constant"""
    return modpow(a, n, pub.n_sq)

def decrypt(priv_l,priv_m, pub, cipher):
    pub_n_sq = pub*pub
    x = pow(cipher, priv_l, pub_n_sq) - 1
    plain = ((x // pub) * priv_m) % pub
    return plain

mapper = {
    'a' : 1,
    'b' : 2,
    'c' : 3,
    'd' : 4,
    'e' : 5,
}

def stringToInteger(ptext):
    num = ""
    for i in range(len(ptext)):
        num = num + str(mapper.get(ptext[i])) + "0"
    return (num)

def decode(num):
    text = str(num)
    ans = ""
    for i in range(len(text)):

        if text[i] != "0":
            for key in mapper.keys():
                if mapper[key] == int(text[i]):
                    ans+=key
        #     for key in mapper.keys():
        #         if mapper[key] == text[i]:
        #             ans += key
            # ans += [key for key, value in mapper.items() if value == int(text[i])][0]        
        #    ans += list(mapper.keys())[list(mapper.values()).index(int(text[i]))]
    return ans

