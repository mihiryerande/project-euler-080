class DecimalArray:
    """
    Class to represent non-negative finite-length decimal numbers as arrays of digits.
    Digits are stored in reverse (least to most significant) for ease of iteration.
    Decimal point location is given by `decimal_places`.
    """

    def __init__(self, int_value=None, digits=None, decimal_places=None, reverse=False) -> None:
        if int_value is not None:
            assert type(int_value) == int and int_value >= 0
            self.digits = list(map(int, list(str(int_value))))[::-1]
            self.decimal_places = 0
        else:
            assert type(digits) == list and all(map(lambda d: type(d) == int and 0 <= d < 10, digits))
            assert type(decimal_places) == int and decimal_places >= 0
            assert type(reverse) == bool
            self.digits = digits[::-1] if reverse else digits
            self.decimal_places = decimal_places
        pass

    def clean(self) -> None:
        # Remove unnecessary zeros from back
        while len(self.digits) > 0 and self.digits[0] == 0 and self.decimal_places > 0:
            self.digits.pop(0)
            self.decimal_places -= 1

        # Remove unnecessary zeros from front
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()

        return

    def floor(self) -> int:
        # Cut off decimal and process back into an int
        # Add extra zero to front in case number has nothing in front of decimal place
        return int(''.join(map(str, (self.digits + [0])[self.decimal_places:][::-1])))

    def __add__(self, other):
        assert type(other) == DecimalArray or (type(other) == int and other >= 0)

        if type(other) == int:
            other = DecimalArray(int_value=other)

        # Add digits sequentially from least to most significant
        digits1 = self.digits.copy()
        digits2 = other.digits.copy()

        # Extend decimal places as needed
        decimals1 = self.decimal_places
        decimals2 = other.decimal_places
        if decimals1 > decimals2:
            digits2 = [0 for _ in range(decimals1 - decimals2)] + digits2
        else:
            digits1 = [0 for _ in range(decimals2 - decimals1)] + digits1
        decimals = max(decimals1, decimals2)

        # Add zeros to front for ease of iteration
        count1 = len(digits1)
        count2 = len(digits2)
        if count1 > count2:
            digits2 += [0 for _ in range(count1 - count2)]
        else:
            digits1 += [0 for _ in range(count1 - count2)]
        count = max(count1, count2)

        # Construct result digit-by-digit
        digits = []
        carry = 0
        for _ in range(count):
            d1 = digits1.pop(0)
            d2 = digits2.pop(0)
            carry, d = divmod(d1 + d2 + carry, 10)
            digits.append(d)
        if carry > 0:
            digits.append(carry)

        result = DecimalArray(digits=digits, decimal_places=decimals)
        result.clean()
        return result

    def __mul__(self, other):
        assert type(other) == DecimalArray or (type(other) == int and 0 <= other < 10)

        if type(other) == int:
            digits1 = self.digits.copy()

            # Figure out digits one-by-one
            # Assuming `other` is a one-digit number,
            #   so digit-wise multiplication won't be a big deal
            digits = []
            carry = 0
            while len(digits1) > 0:
                d1 = digits1.pop(0)
                carry, d = divmod(other * d1 + carry, 10)
                digits.append(d1)

            # Tack on any extra `carry` to front of number
            while carry > 0:
                carry, d = divmod(carry, 10)
                digits.append(d)

            # Decimal place hasn't moved
            result = DecimalArray(digits=digits, decimal_places=self.decimal_places)
            result.clean()
            return result

        else:
            # `other` is also a DecimalArray
            int1 = int(''.join(map(str, self.digits[::-1])))
            int2 = int(''.join(map(str, other.digits[::-1])))

            product = int1 * int2
            digits = list(map(int, list(str(product))))[::-1]
            decimals = self.decimal_places + other.decimal_places

            result = DecimalArray(digits=digits, decimal_places=decimals)
            result.clean()
            return result

            # digits2 = other.digits.copy()

            # result = DecimalArray(int_value=0)
            #
            # # Distributed multiplication of `self` with `other`,
            # #   by individually multiplying each digit by the other number,
            # #   and then shifting and adding the results
            # shift = other.decimal_places
            # while len(digits2) > 0:
            #     d2 = digits2.pop(0)
            #
            #     # Multiplying `self` * (d2 * 10^(-shift))
            #     summand = self * d2
            #     if shift > 0:
            #         summand.decimal_places += shift
            #         if summand.decimal_places > len(summand.digits):
            #             summand.digits += [0 for _ in range(summand.decimal_places - len(summand.digits))]
            #     elif shift < 0:
            #         summand.digits = [0 for _ in range(shift)] + summand.digits
            #
            #     result += summand
            #     shift -= 1
            #
            # result.clean()
            # return result
