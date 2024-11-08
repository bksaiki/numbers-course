# Chapter 1: Fixed-Point Numbers

Quick Links: [Top](../README.md) | [Next](02-fixed-round.md)

Fixed-point numbers are ubiquitous
  in digital signal processing (DSP), microcontrollers,
  hardware accelerators like graphics processing units (GPUs),
  and financial computations.
These numbers are called ``fixed''-point
  since the position of the binary point
  is _fixed_ and will not change.

## Interface

To better under fixed-point numbers,
  we will build a software implementation
  of theme.
In particular,
  we will focus on parts of the implementation
  in line with the theme of this tutorial:
  computer numbers are just interfaces to
  their mathematical counterparts.

To begin,
  we start with the integers.
Specifically,
  we will use the sign-magnitude representation
  of integers: integers are described by a (boolean) sign
  and a (non-negative) magnitude.
Our convention is to refer
  to the sign attribute as `s` and
  the unsigned magnitude attribute as `c`.
```python
class Num():
    s: bool
    """sign"""
    c: int
    """magnitude"""
```
As a side note,
  recall that the sign-magnitude representation
  has a single redundancy: we can represent
  zero by `-0` or `+0`.

To construct a `Num` instance from a native Python integer, say `i`,
  we use a straightforward translation:
```python
x = Num(i < 0, abs(i))
```
Suppose `x` has only `p` significant digits,
  that is, its magnitude can be encoded in
  at most `p` binary digits.
We can visualize these significant digits
  by considering their infinite digit expansion&mdash;an
  infinite sequence of digits separated by
  a binary point that indicates the position
  of the digit in the ones place.
  of digits (all other digits are 0)l

Thus the non-zero digits of `x`
  are contained within a _region of significance_,
  a sequential group of binary digits that contain
  all the non-zero digits in the infinite binary expansion.
Note that we can choose this region of significance
  to be as large as we want, as long as,
  it contains all of the non-zero digits
  and no digit at a position smaller than `exp`.
Therefore,
  we could include zero digits like $b_p$ and $b_{p+1}$
  but not digits such as $b_{-1}$ and $b_{-2}$.
```
... | 0 | 0 | b_{p-1} | b_{p-2} | ... | b_2 | b_1 | b_0 . 0 | 0 | ... 
```
By definition,
  the least significant digit of `x`,
  $b_0$ is immediately to the left of the binary point.

General fixed-point numbers,
  on the other hand, do not have this positional
  restriction that integers have.
Rather,
  the least significant digit is at a fixed
  distance from the binary point,
  either to the left or to the right.
For example,
  we can shift the digits right by 2 places.
```
... | 0 | 0 | b_{p-3} | b_{p-4} | ... | b_{0} . b_{-1} | b_{-2} | 0 | 0 | ... 
```
Our discussion of the region of significance is similar here;
  the region of significance must include
  digits between $-2$ and $p-3$ but can include
  zero digits at positions at or above $p-2$.

To support this, of course,
  our numbers interface needs extending.
We must keep track this least significant digit
  offset for each fixed-point number.
For inspiration,
  we turn to a familiar representation of numbers:
  scientific notation.
Since we are handling binary numbers,
  we use scientific notation using powers of two:
  $$ x = (-1)^s \times c \times 2^{exp} $$
  where `exp` is an integer value called
  the "exponent" of `x`.
Notice that we are using
  "unnormalized" scientific notation
  since `c` is a non-negative integer
  (rather than a value on $[1, 2)$
  as with normalized scientific notation).
As such,
  we will refer to the value `exp`
  as the _unnormalized exponent_ or `x`.

We see that the unnormalized exponent
  is _exactly_ the signed difference of the
  position of the least significant digit to the binary point
  (or more accurately, the digit in the ones place).
Thus,
  the digit offset of `x` is negative
  when `x` contains significant digits
  that are "fractional".
Otherwise,
  `x` is certainly an integer.
(The reverse is not true!)

Returning to our implementation,
  we update the `Num` class with the unnormalized exponent
  attribute `exp`.
```python
class Num():
    s: bool
    """sign"""
    c: int
    """magnitude"""
    exp: int
    """absolute position of the LSB"""
```
Given a number in scientific notation,
  we would initialize as a `Num` instance by writing
```python
x = Num(s, c, exp)
```

## Properties

There are four derived properties
  that are often useful.
The first property is `p`,
  the _precision_ of the value
  which is the minimum number of bits
  required to encode `x.c` in binary.
Notice how this relates to the region of significance:
  the precision `p` is the minimum allowable size
  of the region of significance.
```python
class Num():
    ...
    @property
    def p(self) -> int:
        return self.c.bit_length()
```
The second property is `e`,
  the _normalized_ exponent,
  which represents the exponent of the value
  if we put it in normalized scientific notation
  $(-1)^s \times f \times 2^{\text{e}}$ where $f$ is on $[1, 2)$.
Alternatively,
  this represents the position
  of the most significant digit of `x`.
This operation is not well-defined
  for values that are zero.
By convention,
  we will return `None` making `e`
  an partial function.
```python
class Num():
    ...
    @property
    def e(self) -> Optional[int]:
        if self.c == 0:
            return None
        else:
            return self.exp + self.p - 1
```
The third property is `n`,
  the _absolute digit_ of the value,
  which is the position of the digit
  directly below the least significant digit of `x`.
While this property seems redundant,
  it is useful to differentiate `exp` and `n` later on.
Its definition is straightforward.
```python
class Num():
    ...
    @property
    def n(self) -> int:
        return self.exp - 1
```
The last property is `m`, the _signed_ mantissa.
It is just $(-1)^s \times c$.
```python
class Num():
    ...
    @property
    def m(self) -> int:
        if self.s:
            return -self.c
        else:
            return self.c
```
With these properties defined,
  we can now turn to fixed-point rounding
  in the [next](02-fixed-round.md) section.

### Exercises

Each of the following exercises
  have solutions that can be computed in `O(1)`
  integer operations with respect to `self.p`
  and any other argument.

1. Implement `is_integer(self)` which returns whether
  or not a `Num` value is an integer value.
```python
class Num():
    ...
    def is_integer(self) -> bool:
        ...
```

2. Implement `bit(self, n)` which takes a position `n`
  and returns whether the binary digit at
  that position is `1`.
```python
class Num():
    ...
    def bit(self, n: int) -> bool:
        ...
```

3. Implement `normalize(self, p)` which takes a non-negative precision `p`
  and returns a copy of `self` that satisfies the following properties:
    1. `self` is numerically equivalent to `normalize(self, p)`;
    2. if `self` is non-zero and `self.p <= p`,
      `normalize(self, p)` has exactly `p` bits of precision;
    3. if `self` is non-zero and `self.p > p`,
      `normalize(self, p)` should throw an exception.
```python
class Num():
    ...
    def normalize(self, p: int) -> Num:
        ...
```

4. Implement `split(self, n)` which takes a position `n`
  and returns a pair of `Num` values which represent the digits
  above `n` and the digits at or below `n`.
  If `yh, yl = x.split(n)`,
    then the following properties must be satisfied:
    1. the sum of `yh` and `yl` is numerically equivalent to `x`;
    2. `yh.p <= x.p` and `yl.p <= x.p`;
    3. if `x` is non-zero, then `yh.exp > n` and `yl.exp <= n`;
      regardless of the value of `yh` or `yl`;
    4. `x.s == yh.s` and `x.s == yl.s`
```python
class Num():
    ...
    def split(self, n: int) -> tuple[Num, Num]:
        ...
```
