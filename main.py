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

from math import floor, sqrt

################################################################################
################################## UNFINISHED ##################################
################################################################################

def decimal_floor(digits, count):
    """
    For a finite-length positive decimal number represented as an array of `digits` with `count` decimal places,
      returns the floor of the number as an integer.

    Args:
        digits (List[int]): List of digits in reverse
        count  (int)      : Non-negative integer (<= len(digits))

    Returns:
        (int): Floor of number represented by (digits, count)

    Raises:
         AssertError: if incorrect args are given
    """
    assert type(digits) == list and all(map(lambda d: type(d) == int and 0 <= d < 10, digits))
    assert type(count) == int and 0 <= count <= len(digits)

    # Cut off decimal and process back into an int
    return int(''.join(map(str, digits[count:][::-1])))


def decimal_square(digits, count):
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


def is_square(n):
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


def main(n):
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
    #     Do this by representing finite-length decimal numbers as arrays of digits (in reverse).
    #     To figure out each subsequent digit of sqrt(x),
    #       loop through possible digits [0-9]
    #       and choose the greatest not causing square to exceed `x`.

    digit_sum_all = 0

    for x in range(1, n+1):
        if is_square(x):
            print('Skipping {}'.format(x))
            continue
        else:
            print('Calculating {} ...'.format(x))

            # Start with the closest whole number, so no decimal digits yet
            approx_root = list(map(int, list(str(floor(sqrt(x))))))
            approx_root.reverse()

            # Add each next digit sequentially, until 100 digits found
            for root_digit_count in range(1, 101):  # Number of decimal places of current approx_root
                # Next digit is in range [0-9], so try from 9 downwards until square becomes less than `x`
                approx_root.insert(0, None)
                for d in range(9, -1, -1):
                    approx_root[0] = d
                    if d == 0:
                        # No compute needed since 0 is the last digit option
                        break
                    else:
                        approx_square, square_digit_count = decimal_square(approx_root, root_digit_count)
                        if decimal_floor(approx_square, square_digit_count) < x:
                            # Square of approx_root is less than `x`, so digit `i` has been found
                            break
                        else:
                            continue

            digit_sum = sum(approx_root[:100])
            print('  -> {}'.format(digit_sum))
            digit_sum_all += digit_sum

    return digit_sum_all


if __name__ == '__main__':
    maximum_square = int(input('Enter a natural number: '))
    decimal_digit_sum = main(maximum_square)
    print('Sum of first 100 decimal digits of irrational square roots through {}:'.format(maximum_square))
    print('  {}'.format(decimal_digit_sum))
