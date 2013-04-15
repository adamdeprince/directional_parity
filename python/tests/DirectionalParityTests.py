from directional_parity.encoder import encode, limit
from directional_parity.decoder import decode
from unittest import TestCase

TEST_BITS = range(3, 14, 2)

class TestDirectionalParity(TestCase):
    "Directional Parity Tests"

    def mutate(self, seq):
        return seq

    def test_encode_decode(self):
        "decode(encode(value)) returns value"

        for b in TEST_BITS:
            print "Test", b
            for expected in range(limit(b)):
                encoding = encode(b, expected)
                encoding = self.mutate(encoding)
                actual = decode(encoding)
                self.assertEquals(actual,
                                  expected,
                                  msg = "Bits: %d, expected: %d, actual: %d, encoding: %s" % (b, expected, actual, encoding))

    
class TestReversedParity(TestDirectionalParity):
    "Confirm all tests work on reversed strings"
    def mutate(self, seq):
        return list(reversed(seq))


TF = [False, True]

class ConfirmMatchesWNYCJavascript(TestCase):
    "Confirm outputs match WNYCJavascript Testcase"

    @staticmethod
    def parse_nibble(a, b, c, d):
        a = int(bool(int(a)))
        b = int(bool(int(b)))
        c = int(bool(int(c)))
        d = int(bool(int(d)))
        return a + b*2 + c*4 + d*8
        
    @classmethod
    def parse_reversible_9bit_sequence(cls, a, b, c, d, e, i, h, g, f):
        e = bool(int(e))
        low = cls.parse_nibble(a, b, c, d)
        high = cls.parse_nibble(f, g, h, i)
        if (e and (low == high)):
            return 256 + low
        if (e != (low > high)):
            (low, high) = (high, low)
        return low + high * 16

    def test_parse(self):
        for a in TF:
            for b in TF:
                for c in TF:
                    for d in TF:
                        for e in TF:
                            for f in TF:
                                for g in TF:
                                    for h in TF:
                                        for i in TF:
                                            seq = (a, b, c, d, e, f, g, h, i)
                                            expected = self.parse_reversible_9bit_sequence(*seq)
                                            actual = decode(seq)
                                            self.assertEquals(expected, actual, msg="seq(%s) expected: %s acutal: %s" % (seq, expected, actual))

                                
        
        
        
        
        
