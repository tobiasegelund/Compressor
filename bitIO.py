
# Based on http://rosettacode.org/wiki/Bitwise_IO#Python

class BitWriter(object):
    def __init__(self, f):
        self.accumulator = 0 # the int buiding up to a full byte to be written
        self.bcount = 0 # number of bits pun in the accumulator so far
        self.out = f # the file object we are writing to

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

    def __del__(self):
        try:
            self.flush()
        except ValueError:   # I/O operation on closed file.
            pass

    def writebit(self, bit):
        if self.bcount == 8:
            self.flush()
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount += 1

    def _writebits(self, bits, n):
        while n > 0:
            self.writebit(bits & 1 << n-1)
            n -= 1

    def writeint32bits(self, intvalue):
        self._writebits(intvalue, 32)

    def flush(self):
        if self.bcount: # if any bits have accumulated
            self.out.write(bytearray([self.accumulator]))
            self.accumulator = 0
            self.bcount = 0

class BitReader(object):
    def __init__(self, f):
        self.input = f # the file object we are reading from
        self.accumulator = 0 # cache of the last byte read
        self.bcount = 0 # number of bits left unread in accumulator
        self.read = 0 # Was last read succesful? [EOF or not?]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def readsucces(self):
        return self.read

    def readbit(self):
        if not self.bcount: # if bcount == 0 [no unread bits in accumulator]
            a = self.input.read(1)
            if a: # if not EOF [EOF = attempt at reading returns empty list]
                self.accumulator = ord(a) # int between 0 and 256, [note that
                                          # ord works for byte objects]
            self.bcount = 8 # number of bits available
            self.read = len(a) # remember number of bytes read (0 => EOF)
        # extract the (bcount-1)'th bit [the next bit] in the accumulator:
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1 # move to next bit in accumulator
        return rv

    def _readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v

    def readint32bits(self):
        return self._readbits(32)
