import random

# Генератор карт
# decimal_decoder = lambda s: int(s, 10)
# decimal_encoder = lambda i: str(i)

class Card_Generator(object):
    @staticmethod
    def luhn_sum_mod_base(s):
        digits = [int(c) for c in s]
        b = 10
        return (sum(digits[::-2]) +
                sum(sum(divmod(2 * d, b)) for d in digits[-2::-2])) % b

    @staticmethod
    def verify(s):
        return Card_Generator.luhn_sum_mod_base(s) == 0

    @staticmethod
    def generate(s):
        d = Card_Generator.luhn_sum_mod_base(s + '0')
        if d != 0:
            d = 10 - d
        return str(d)

    @staticmethod
    def generate_pan(pan_len=16):
        prefix = '510000'
        base = prefix + str(random.randint(
            10 ** (pan_len - len(prefix) - 2),
            10 ** (pan_len - len(prefix) - 1) - 1))
        pan = base + Card_Generator.generate(base)
        assert Card_Generator.verify(pan)
        return pan