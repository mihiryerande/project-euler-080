# Problem 80:
#     Square Root Digital Expansion
#
# Description:
#     It is well known that if the square root of a natural number is not an integer, then it is irrational.
#     The decimal expansion of such square roots is infinite without any repeating pattern at all.
#
#     The square root of two is 1.41421356237309504880...,
#       and the digital sum of the first one hundred decimal digits is 475.
#
#     For the first one hundred natural numbers,
#       find the total of the digital sums of the first one hundred decimal digits
#       for all the irrational square roots.

from decimal_array import DecimalArray
from math import floor, sqrt
from typing import List, Tuple


def decimal_square(digits: List[int], count: int) -> Tuple[List[int], int]:
    """
    For a finite-length positive decimal number represented as an array of `digits` with `count` decimal places,
      returns the square of the number as a tuple represented in the same way.

    Args:
        digits (List[int]): List of digits in reverse
        count  (int)      : Non-negative integer (<= len(digits))

    Returns:
        (List[int], int):
            Tuple of ...
              * List of digits of squared number, in reverse
              * Count of decimal places in digit list

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(digits) == list and all(map(lambda d: type(d) == int and 0 <= d < 10, digits))
    assert type(count) == int and 0 <= count <= len(digits)

    # Ignore decimal place first, and square the full number
    x = int(''.join(map(str, digits[::-1])))
    x = x ** 2
    x = list(map(int, list(str(x))[::-1]))
    return x, 2*count


def is_square(n: int) -> bool:
    """
    Returns True iff `n` is a square number.

    Args:
        n (int): Natural number

    Returns:
        (bool): True iff `n` is a square number

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0
    r = sqrt(n)
    return floor(r) == r


def main(n: int) -> int:
    """
    For the first `n` natural numbers,
      returns the sum of the first 100 decimal digits
      of all the irrational square roots.

    Args:
        n (int): Natural number

    Returns:
        (int): Sum of first 100 decimal digits of all irrational square roots of natural numbers at most `n`

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Idea:
    #     Simply figure out the 100 digits of each number up through `n`.
    #     Do this by representing a finite-length decimal number as a DecimalArray (array of digits in reverse).
    #     To figure out each subsequent digit of sqrt(x),
    #       loop through possible digits [0-9]
    #       and choose the greatest not causing square to exceed `x`.

    # Future improvements:
    #   * Rather than linearly searching for each digit [0-9], use binary search for some speedup.
    #   * Use some algebraic manipulation to directly figure out the best next digit (?)

    digit_sum_all = 0

    for x in range(1, n+1):
        if is_square(x):
            continue
        else:
            # Start with the closest whole number, so no decimal digits yet
            approx_root = DecimalArray(int_value=floor(sqrt(x)))

            # Add each next digit sequentially, until 100 digits found
            while len(approx_root.digits) < 100:
                # Next digit is in range [0-9], so try from 9 downwards until square becomes less than `x`
                approx_root.digits.insert(0, None)
                approx_root.decimal_places += 1
                # print('    Temp root = {}, {}'.format(approx_root.digits, approx_root.decimal_places))
                for d in range(9, -1, -1):
                    approx_root.digits[0] = d
                    if d == 0:
                        # No compute needed since 0 is the last digit option
                        break
                    else:
                        approx_square = approx_root * approx_root
                        if approx_square.floor() < x:
                            # Square of approx_root is less than `x`, so digit `i` has been found
                            break
                        else:
                            continue
            # Extract first 100 digits of number, regardless of decimal place
            digit_sum = sum(approx_root.digits[-100:])
            digit_sum_all += digit_sum

    return digit_sum_all


if __name__ == '__main__':
    maximum_square = int(input('Enter a natural number: '))
    decimal_digit_sum = main(maximum_square)
    print('Sum of first 100 decimal digits of irrational square roots through {}:'.format(maximum_square))
    print('  {}'.format(decimal_digit_sum))
