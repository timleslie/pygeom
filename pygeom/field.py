"""
This module contains classes which implement various different fields.

Recall that a mathematical field is a set of "numbers" which are closed under
the four basic operations of addition, subtraction, multiplication and division.

All calculations performed by pygeom are done over a specific field and thus
this is very core of the package.
"""

import random

from pygeom.util import inverse, gcd, isqrt, is_square, shanks_tonelli

class Field(object):
    """
    This base class provides the interface for numbers within a given field.    

    All field classes must implement the full interface defined here to be able
    to be used by pygeom.
    """

    def __init__(self, value, *args, **kwargs):
        pass

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __div__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __rmul__(self, other):
        raise NotImplementedError

    def __rdiv__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not bool(self == other)

    def is_square(self):
        """
        Boolean function to check if the number is a square in the field.

        E.g. for a given :math:`x \in F`, does there exist an :math:`a \in F` such that :math:`a^2 = x`.

        :rtype: Boolean
        """
        raise NotImplementedError

    def sqrt(self):
        """
        The square root of the number in the field.

        Returns the value :math:`a \in F` such that :math:`a^2 = x`.

        :raises: ValueError if no such :math:`a` exists.
        """
        raise NotImplementedError

    def reduce(self, others):
        """
        Reduce this number, along with a list of others so that all common
        factors are removed.
        """
        raise NotImplementedError

    @classmethod
    def random(cls):
        raise NotImplementedError    

class FiniteField(Field):

    base = 3

    def __init__(self, value, base=None):
        Field.__init__(self, value)

        # We're actually pedantic about types here.
        if type(value) not in [int, long]:
            raise TypeError
        if base is None:
            self._base = self.base
        elif type(base) not in [int, long]:
            raise TypeError, "base must be a prime number (%s)" % str(base)
        elif base <= 1:
            raise ValueError, "base must be a prime number (%s)" % str(base)
        else:
            self._base = base

        # Convert to a value between [0, base-1]
        self.value = value % self._base

    def __repr__(self):
        return "%d (%d)" % (self.value, self._base)

    def _op(self, op, other):
        """
        Perform an operator on this and another object.
        """
        if other.__class__ == self.__class__:
            return self.__class__(op(other.value), self._base)
        elif type(other) in [int, long]:
            return self.__class__(op(other), self._base)
        else:
            raise TypeError

    def __add__(self, other):
        return self._op(self.value.__add__, other)

    def __sub__(self, other):
        return self._op(self.value.__sub__, other)

    def __mul__(self, other):
        try:
            return self._op(self.value.__mul__, other)
        except TypeError:
            try:
                return other.__rmul__(self)
            except:
                raise TypeError

    def __neg__(self):
        return self.__class__(0, self._base) - self

    def __div__(self, other):
        if other.__class__ == self.__class__:
            return self * inverse(other.value, self._base)
        elif type(other) in [int, long]:
            return self * inverse(other, self._base)
        else:
            raise TypeError

    def __radd__(self, other):
        return self._op(self.value.__add__, other)

    def __rsub__(self, other):
        return self._op((-self.value).__add__, other)

    def __rmul__(self, other):
        return self._op(self.value.__mul__, other)

    def __rdiv__(self, other):
        return self.__class__(other * inverse(self.value, self._base),
                              self._base)

    def __eq__(self, other):
        if type(other) in [int, long]:
            other = self.__class__(other, self._base)

        if other.__class__ == self.__class__:
            return self.value == other.value and self._base == other._base
        else:
            raise TypeError, "Equality not defined for (%s)" % str(other)

    def is_square(self):
        """
        Boolean function to check if the number is a square in the field.

        E.g. for a given x \in F, does there exist an a \in F such that a*a = x.

        If x is a square then x^(p - 1)/2 = 1 (mod p).

        :rtype: Boolean
        """        
        result = 1
        for _ in range((self._base - 1)/2):
            result *= self.value
        return result % self._base == 1 or self.value == 0

    def sqrt(self):
        """
        The square root of the number in the field.

        Returns the value a \in F such that a*a = x.

        If no such a exists, raises ValueError.
        """
        if not self.is_square():
            raise ValueError, "This number is not a square! (%s)" % str(self)
        a = self.__class__(shanks_tonelli(self.value, self._base))
        assert a*a == self
        return a

    def reduce(self, others):
        """
        Reduce this number, along with a list of others so that all common
        factors are removed.
        """
        if self == 0:
            if others:
                return [self] + others[0].reduce(others[1:])
            else:
                return [self]
        else:
            return [self/self] + [x/self for x in others]
        
    @classmethod
    def random(cls):
        """
        Return a random field object.
        """
        return cls(random.randint(0, cls.base - 1))

class Rational(Field):

    _min_random = -10
    _max_random = 10

    def __init__(self, num, den=1):
        Field.__init__(self, (num, den))
        self.num = num
        self.den = den
        if self.den == 0:
            raise ValueError, "Denominator in rational cannot be zero"
        if type(self.num) not in [int, long]:
            raise TypeError, "Numerator must be an integer (%s)" % str(self.num)
        if type(self.den) not in [int, long]:
            raise TypeError, \
                "Denominator must be an integer (%s)" % str(self.den)
        self._reduce()

    def __repr__(self):
        return "%d/%d" % (self.num, self.den)

    def _reduce(self):
        """
        Reduce the values to remove any common factors.
        """
        gcd_ = gcd(self.num, self.den)
        self.num /= gcd_
        self.den /= gcd_

    def _get_num_den(self, other):
        """
        Return a (numerator, denominator) pair for the given value. Handles
        both Rationals and regular integers. Other types will raise a
        TypeError
        """
        if type(other) in [int, long]:
            return other, 1
        elif other.__class__ == self.__class__:
            return other.num, other.den
        else:
            raise TypeError, str(self.__class__) + str(other.__class__)

    def __add__(self, other):
        a1, b1 = self.num, self.den
        a2, b2 = self._get_num_den(other)
        return Rational(a1*b2 + a2*b1, b1*b2)

    def __sub__(self, other):
        a1, b1 = self.num, self.den
        a2, b2 = self._get_num_den(other)
        return Rational(a1*b2 - a2*b1, b1*b2)

    def __mul__(self, other):
        a1, b1 = self.num, self.den
        try:
            a2, b2 = self._get_num_den(other)
        except TypeError:
            try:
                x = other.__rmul__(self)
                if x == NotImplemented:
                    raise NotImplementedError
                return x
            except:
                raise TypeError
        return Rational(a1*a2, b1*b2)

    def __neg__(self):
        a1, b1 = self.num, self.den
        return Rational(-a1, b1)

    def __div__(self, other):
        a1, b1 = self.num, self.den
        a2, b2 = self._get_num_den(other)
        if b1*a2 == 0:
            raise ZeroDivisionError
        return Rational(a1*b2, b1*a2)

    def __radd__(self, other):
        return self + other 

    def __rsub__(self, other):
        return (-self) + other

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        a1, b1 = self.num, self.den
        if a1 == 0:
            raise ZeroDivisionError
        return other * Rational(b1, a1)

    def __eq__(self, other):
        if type(other) in [int, long]:
            return self.num == other and self.den == 1
        elif other.__class__ == self.__class__:
            return other.num == self.num and other.den == self.den
        else:
            raise TypeError, "Equality not defined for (%s)" % str(other)

    def is_square(self):
        """
        Boolean function to check if the number is a square in the field.

        E.g. for a given x \in F, does there exist an a \in F such that a*a = x.
        """
        return is_square(self.num) and is_square(self.den)

    def sqrt(self):
        """
        The square root of the number in the field.

        Returns the value a \in F such that a*a = x.

        If no such a exists, raises ValueError.
        """
        if self.is_square():
            return Rational(isqrt(self.num), isqrt(self.den))
        else:
            raise ValueError, "%s is not a square" % str(self)

    def reduce(self, others):
        """
        Reduce this number, along with a list of others so that all common
        factors are removed.
        """
        if self == 0:
            if others:
                return [self] + others[0].reduce(others[1:])
            else:
                return [self]

        common_denom = self.den
        for x in others:
            common_denom *= x.den


        self = self*common_denom
        others = [x*common_denom for x in others]

        gcd_ = self.num
        for x in others:
            gcd_ = gcd(gcd_, x.num)

        self = self.__div__(gcd_)
        others = [x/gcd_ for x in others]
        return [self] + others


    @classmethod
    def random(cls):
        """
        Return a random field object.
        """
        num = random.randint(cls._min_random, cls._max_random)
        den = random.randint(cls._min_random, cls._max_random)
        if den == 0:
            den = 1
        return cls(num, den)
                              

