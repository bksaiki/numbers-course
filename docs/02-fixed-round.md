# Chapter 2: Fixed-Point Rounding

Quick Links: [Top](../README.md) | [Previous](01-fixed.md) | [Next](03-fixed-overflow.md)

In the previous section,
  we discussed representing numbers with
  a fixed (least significant) digit position relative
  to the binary point (the position of the ones place).
In particular,
  we relate this position constraint to unnormalized
  scientific numbers, that is, an integer scaled
  by some power of 2: $m \times 2^{exp}$.
But, what if we wish to change
  the position of this least significant digit?

In the first case,
  consider what happens if we wish to move the position
  of the least significant digit, `exp`, by some negative
  amount, say `d`.
In other words,
  we wish this new value to be numerically equivalent to
  the original value but includes less significant digits
  in its representation.
This operation is fairly straightforward.
Since we are decreasing `exp` the digits of `c`
  shift left _relative_ to the position of
  the least significant digit.
Note that if `y = shift_right(x, d)`
  and `x` represents a non-zero value,
  then `y.p == x.p + d`.
We illustrate this operation below.
```python
class Num():
    ...
    def shift_right(self, d: int) -> Num:
        if d < 0:
            raise ValueError('must be non-negative', d)
        else:
            exp = self.exp - d
            c = self.c << d
            return Num(self.s, exp, c)
```
Convince yourself that this implementation
  also works for values that represent zero.
You may have noticed that the solutions to exercises
  in the previous section often required handling
  values representing zero in a separate case.
In general,
  this is a good design principle for implementations
  of number systems, but it is not always necessary;
  careful analysis may allow you to eliminate
  these extraneous special cases.

Now consider the other case,
  where we shift the the position
  of the least significant digit, `exp`,
  by some positive amount, say `d`.
In other words,
  we wish this new value to be numerically equivalent to
  the original value but its least significant digit
  is more significant than before.
The problem is satisfying both of these constraints:
  what if we have a non-zero binary digit
  that is between `[exp, exp + d)`?
Clearly,
  the new number cannot represent this digit since it
  is below the region of significance.
If we choose to
  just "drop" these non-zero digits,
  then the new value will not be numerically
  equivalent to the old value.
Mathematically,
  this operation would correspond
  to introducing a perturbation, $\varepsilon$
  to the original value, that is,
  the new value is some $x + \varepsilon$.

## Rounding

This "loss" of digits is the fundamental issue
  that a _rounding_ operation intends to address.
In this case,
  a rounding operation must decide a _representable_ value `x'`
  for a given fixed-point value `x` when digits are lost.
Ideally,
  `x'` is "close" to `x` for some metric
  that is important to users of this number representation,
  and the operation is computable in a reasonable
  amount of time.

## Rounding Contexts

To describe the parameters required to
  carry out a rounding operation,
  we encapsulate this information in
  an object called a _rounding context_.
A rounding operation takes both a value `x`
  and a rounding context `ctx` to decided
  a "best" value `x'`.
Any value that is representable
  according the rounding context is
  said to be representable _under_
  the rounding context.
Clearly,
  rounding fixed-point values to other fixed-point
  values requires a new least significant digit.
```python
class RoundingContext():
    exp: int
    """position of the least significant digit"""
```
Assuming that `x` is not representable
  under the rounding context,
  it is between two representable values,
  say `y1` and `y2`.
We need a way to decide which of these values
  to decide deterministically.
We call this deciding information,
  the _rounding mode_ of the rounding context.


### Exercises

1. In this section,
  we discussed the notion of numerical equivalence,
  that is values representing the same real number,
  but not necessarily containing the same in-memory data.
Implement a check for numerical equivalence.
```python
class Num():
    ...
    def equiv(self, other: Num) -> bool:
        ...
```

2. We showed that the "shift_left" counterpart
  of `shift_right` would introduce a perturbation, $\varepsilon$.
Prove that for a non-zero argument,
  $\varepsilon$ must bounded above in magnitude by $2^{exp + d}$.
