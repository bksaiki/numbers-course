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

    def __init__(self, s: bool, c: int, exp: int):
        if not isinstance(s, bool):
            raise ValueError('expected a boolean', s)
        if not isinstance(c, int) or c < 0:
            raise ValueError('expected a non-negative integer', c)
        if not isinstance(exp, int):
            raise ValueError('expected an integer', exp)
        
        self.s = s
        self.c = c
        self.exp = exp

    @property
    def p(self) -> int:
        """
        Minimum number of binary digits required to encode `self.c`.
        """
        return self.c.bit_length()

    @property
    def e(self) -> Optional[int]:
        """
        Position of the most significant digit. Returns `None` if this value is zero.
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
        Returns whether this value represents an integer.
        """
        # special case: 0 is an integer
        if self.is_zero():
            return True
        
        # all significant digits are integer digits
        if self.exp >= 0:
            return True
        
        # all significant digits are fractional digits
        assert self.e is not None
        if self.e < 0:
            return False

        # must check if fractional bits are zero
        mask = bitmask(-self.exp)
        fbits = self.c & mask
        return fbits == 0

