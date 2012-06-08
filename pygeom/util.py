def egcd(a, b):
    """
    Perform the extended euler algorithm to find, x, y, g such that x*a + y*b = g
    """
    # pylint: disable-msg=C0103

    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def gcd(a, b):
    """
    Calculate the greatest common divisor of two integers a and b.
    """
    return egcd(a, b)[2]

def inverse(a, p):
    """
    Return x such that a*x == 1 (mod p).
    """
    if a == 0:
        raise ZeroDivisionError
    return egcd(a, p)[0]

def isqrt(n):
    """
    Integer square root

    Uses the integer square root algorithm described at:
    http://en.wikipedia.org/wiki/Integer_square_root
    """    
    xn = 1
    xn1 = (xn + n/xn)/2
    while abs(xn1 - xn) > 1:
        xn = xn1
        xn1 = (xn + n/xn)/2
    while xn1*xn1 > n:
        xn1 -= 1
    return xn1

def is_square(n):
    """
    Check whether an integer is a square root.
    """
    return n >= 0 and isqrt(n)**2 == n

def shanks_tonelli(n, p):
    """
    For a given n solve x^2 = n (mod p), where p is an odd prime and n is a
    quadratic residue of p

    Reference: http://planetmath.org/encyclopedia/ShanksTonelliAlgorithm.html
    """
    # pylint: disable-msg=C0103
    
    if n == 0:
        return 0

    # 1. First find positive integers Q and S such that
    # p - 1 = (2^S)*Q, where Q is odd. 

    Q = p - 1
    S = 0
    while Q % 2 == 0:
        S += 1
        Q /= 2

    assert Q * 2**S == p - 1
    assert Q % 2 == 1

    # 2. Then find a quadratic nonresidue W of p and compute V = W^Q(modp) 

    W = 2
    while True:
        result1 = W**((p-1)/2) % p
        result = 1
        for _ in range((p - 1)/2):
            result *= W
            result %= p
        assert result == result1
        if result != 1:
            break
        W += 1

    V = 1
    for _ in range(Q):
        V *= W
        V %= p

    assert V == W**Q % p

    # 3. Then find an integer n' that is the multiplicative inverse of 
    # n (mod p) (i.e., n'*n = 1 (mod p) ).
    nn = inverse(n, p)

    assert (nn * n) % p == 1
        
    # 4. Compute R = n^((Q+1/2))(modp)
    R = 1
    for _ in range((Q+1)/2):
        R *= n
        R %= p
    assert n**((Q+1)/2) % p == R

    while True:

        # 5. and find the smallest integer i >= 0 that satisfies 
        # (R^2*n')^(2^i) = 1 (mod p)
        i = 0
        RR = R*R*nn % p
        while RR != 1:
            RR *= RR
            RR %= p
            i += 1

        assert (R*R*nn)**(2**i) % p == 1

        # 6. If i=0, then x=R, and the algorithm stops. 
        if i == 0:
            break
            
        # 7. Otherwise, compute R' = R*V^2^(S-i-1) (mod p) and repeat the 
        # procedure for R = R'.
        RR = R*(V**(2**(S - i - 1))) % p
        assert RR % p == R*(V**(2**(S - i - 1))) % p
        R = RR

    assert R*R % p == n % p
    return R

class GeometryError(Exception): pass

class NullLineError(Exception): pass

def check_geometry(func):
    def _check_geometry(*items):
        geometries = [item.geometry for item in items if hasattr(item, "geometry")]
        if None in geometries:
            i = geometries.index(None)
            raise GeometryError, "Object %d (%s) has no geometry." % \
                (i, items[i])
        geom0 = geometries[0]
        equal_geoms = [geom == geom0 for geom in geometries]
        if False in equal_geoms:
            i = equal_geoms.index(False)
            raise GeometryError, \
                "Object %d (%s) has a different geometry to the first (%s)" % \
                (i, geometries[i], geom0)
        return func(*items)
    return _check_geometry

def M(a, b):
    """
    Calculate the symmetric M matrix.
    """
    return a*a, a*b, b*b

def all_equal(objects):
    if objects == []:
        return True
    basis = objects[0]
    return False not in [basis == obj for obj in objects]
