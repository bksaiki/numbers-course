

def bitmask(k: int):
    """Creates a bitmask that is all 1s for the first `k`-bits."""
    if not isinstance(k, int) or k < 0:
        raise ValueError('must be a non-negative integer', k)
    return (1 << k) - 1
