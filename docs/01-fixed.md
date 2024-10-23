## Chapter 1: Fixed-Point Numbers

Quick Links: [Top](../README.md) | [Next](02-fixed-round.md)

Fixed-point numbers are ubiquitous
  in digital signal processing (DSP), microcontrollers,
  hardware accelerators like graphics processing units (GPUs),
  and financial computations.
These numbers are called ``fixed''-point
  since the position of the binary point
  is _fixed_ and will not change.

Start with an integer representation in
  sign-magnitude form, that is,
  we separately store the sign, represented by a boolean,
  and the magnitude, represented by a non-negative integer.
Our convention is to
  name the sign attribute `s` and
  the unsigned magnitude attribute `c`.
```python
class Num():
    s: bool
    """sign of this number"""
    c: int
    """magnitude of this number"""
```
We can visualize the magnitude of an `Num` value
  by placing its significant digits, say $p$ of them,
  within an infinite sequence of binary digits,
  of which only the significant digits may be `1`.
The sequence also contains
  a binary point to indicate the position
  of the ones place.
```
... | 0 | 0 | b_{p-1} | b_{p-2} | ... | b_2 | b_1 | b_0 . 0 | 0 | ... 
```
Notice that the binary point is just
  below the the least significant digit
  $b_0$ of the value.
For fixed-point values in general,
  we shift where the $p$ significant values are.
For example,
  we can shift the digits right by 2 places.
```
... | 0 | 0 | b_{p-3} | b_{p-4} | ... | b_{0} . b_{-1} | b_{-2} | 0 | 0 | ... 
```
In our implementation,
  we track the position of our significant digits
  by storing the absolute position of
  the least significant digit.
Our convention is to name the
  this absolute position attribute `exp`.
We usually refer to its value as
  the _unnormalized_ exponent since we can view
  values in this representation as numbers
  in unnormalized scientific notation
  $(-1)^s \times c \times 2^{\text{exp}}$.
```python
class Num():
    s: bool
    """sign of this number"""
    c: int
    """magnitude of this number"""
    exp: int
    """absolute position of the LSB"""
```
In the example above,
  we would set `exp` to `-2` when
  initializing a value in that representation.

There are four derived properties
  that are often useful.
The first property is `p`,
  the _precision_ of the value
  which is the minimum number of bits
  required to encode `c` in binary.
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
  $(-1)^s \times f \times 2^{\text{e}}$ where $f$ is on $[0, 1]$.
We should be careful about values that are zero
  since this operation is not well-defined.
By convention,
  we just extend its definition for non-zero values;
  peculiarly, `x = 0` iff `e() < exp()`.
```python
class Num():
    ...
    @property
    def e(self) -> int:
        return self.exp + self.p - 1
```
The third property is `n`,
  the _absolute digit_ of the value,
  which is the first digit that is not significant.
Its definition is simple.
```python
class Num():
    ...
    @property
    def n(self) -> int:
        return self.exp - 1
```
The last property is `m`, the _signed_ mantissa.
It is just $(-1)^s \times m$.
```python
class Num():
    ...
    @property
    def m(self) -> int:
        if self.s
            return -self.m
        else
            return self.m
```
With these properties defined,
  we can now turn to fixed-point rounding
  in the [next](02-fixed-round.md) section.

### Exercises

1. Implement `is_integer()` which returns whether
  or not a `Num` value is integer value.
```python
class Num():
    ...
    def is_integer(self) -> bool
        ...
```

2. Implement `split(n)` which takes a position `n`
  and returns a pair of `Num` values which
  represent the digits above `n` and the digits
  at or below `n`.
```python
class Num():
    ...
    def split(self, n: int) -> tuple[Num, Num]
        ...
```

3. Implement `bit(n)` which takes a position `n`
  and returns whether the binary digit at
  that position is `1`.
```python
class Num():
    ...
    def bit(self, n: int) -> bool
        ...
```
