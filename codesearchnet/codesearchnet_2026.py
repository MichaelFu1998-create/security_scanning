def digest(self):
    """Terminate the message-digest computation and return digest.

    Return the digest of the strings passed to the update()
    method so far. This is a 16-byte string which may contain
    non-ASCII characters, including null bytes.
    """

    A = self.A
    B = self.B
    C = self.C
    D = self.D
    input = [] + self.input
    count = [] + self.count

    index = (self.count[0] >> 3) & 0x3f

    if index < 56:
      padLen = 56 - index
    else:
      padLen = 120 - index

    padding = [b'\200'] + [b'\000'] * 63
    self.update(padding[:padLen])

    # Append length (before padding).
    bits = _bytelist2long(self.input[:56]) + count

    self._transform(bits)

    # Store state in digest.
    digest = struct.pack("<IIII", self.A, self.B, self.C, self.D)

    self.A = A
    self.B = B
    self.C = C
    self.D = D
    self.input = input
    self.count = count

    return digest