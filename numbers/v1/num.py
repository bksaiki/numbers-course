from typing import Optional

from ..utils import bitmask

class Num(object):
    """
    Fixed-point numbers, as implemented in Chapter 1.
    """

    s: bool
    """
    sign
    """
    c: int
    """
    (unsigned) magnitude
    """
    exp: int
    """
    absolute position of the LSB
    """

    def __init__(self, s: bool, exp: int, c: int):
        if not isinstance(s, bool):
            raise ValueError('expected a boolean', s)
        if not isinstance(exp, int):
            raise ValueError('expected an integer', exp)
        if not isinstance(c, int) or c < 0:
            raise ValueError('expected a non-negative integer', c)
        
        self.s = s
        self.c = c
        self.exp = exp

    def __repr__(self):
        return 'Num(s=' + repr(self.s) + ', exp=' + repr(self.exp) + ', c=' + repr(self.c) + ')'

    @property
    def p(self) -> int:
        """
        Minimum number of binary digits required to encode `self.c`.
        """
        return self.c.bit_length()

    @property
    def e(self) -> Optional[int]:
        """
        Position of the most significant digit.
        Returns `None` if this value is zero.
        """
        if self.c == 0:
            return None
        else:
            return self.exp + self.p - 1

    @property
    def n(self) -> int:
        """
        Position of the first unrepresentable digit below the significant digits.
        This is exactly `self.exp - 1`.
        """
        return self.exp - 1
    
    @property
    def m(self) -> int:
        """
        Signed significand.
        This is exactly `(-1)^self.s * self.c`.
        """
        if self.s:
            return -self.m
        else:
            return self.m
        
    def is_zero(self) -> bool:
        """
        Returns whether this value represents zero.
        """
        return self.c == 0

    def is_integer(self) -> bool:
        """
        Exercise 1.1:
        Returns whether this value represents an integer.
        """
        # special case: 0 is an integer
        if self.is_zero():
            return True
        
        assert self.e is not None
        
        # all significant digits are integer digits
        if self.exp >= 0:
            return True
        
        # all significant digits are fractional digits
        if self.e < 0:
            return False

        # must check if fractional bits are zero
        mask = bitmask(-self.exp)
        fbits = self.c & mask
        return fbits == 0

    def bit(self, n: int) -> bool:
        """
        Exercise 1.2:
        Returns the value of the digit at the `n`th position as a boolean.
        """
        if not isinstance(n, int):
            raise ValueError('expected an integer', n)

        # special case: 0 has no digits set
        if self.is_zero():
            return False
    
        assert self.e is not None

        # below the region of significance
        if n < self.exp:
            return False
        
        # above the region of significane
        if n > self.e:
            return False
        
        idx = n - self.exp
        bit = self.c & (1 << idx)
        return bit != 0
    

    def normalize(self, p: int):
        """
        Exercise 1.3:
        Returns a copy of `self` that has exactly `p` bits of precision.
        If `p < self.p`, a `ValueError` is thrown.
        """
        if not isinstance(p, int) or p < 0:
            raise ValueError('expected a non-negative integer', p)
        
        # special case: 0 has no precision ever
        if self.is_zero():
            return self
        
        # check that the requested precision is enough
        if p < self.p:
            raise ValueError('insufficient precision', self, p)
        
        shift = p - self.p
        exp = self.exp - shift
        c = self.c << shift
        return Num(self.s, exp, c)
        
    def split(self, n: int):
        """
        Exercise 1.4:
        Splits `self` into two `Num` values where the first value represents
        the digits above `n` and the second value represents the digits below `n`.
        """
        if not isinstance(n, int):
            raise ValueError('expected an integer', n)
        
        # special case: 0 has no precision
        if self.is_zero():
            hi = Num(self.s, n + 1, 0)
            lo = Num(self.s, n, 0)
            return (hi, lo)
        
        assert self.e is not None

        # check if all digits are in the lower part
        if n > self.e:
            hi = Num(self.s, n + 1, 0)
            lo = Num(self.s, self.exp, self.c)
            return (hi, lo)
        
        # check if all digits are in the upper part
        if n < self.exp:
            hi = Num(self.s, self.exp, self.c)
            lo = Num(self.s, n, 0)
            return (hi, lo)
        
        # splitting the digits
        p_lo = (n + 1) - self.exp
        mask_lo = bitmask(p_lo)
        
        exp_hi = self.exp + p_lo
        c_hi = self.c >> p_lo

        exp_lo = self.exp
        c_lo = self.c & mask_lo

        hi = Num(self.s, exp_hi, c_hi)
        lo = Num(self.s, exp_lo, c_lo)
        return (hi, lo)

