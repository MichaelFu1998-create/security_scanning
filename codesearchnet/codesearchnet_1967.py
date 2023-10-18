def _transform(self, W):

        for t in range(16, 80):
            W.append(_rotateLeft(
                W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16], 1) & 0xffffffff)

        A = self.H0
        B = self.H1
        C = self.H2
        D = self.H3
        E = self.H4

        """
        This loop was unrolled to gain about 10% in speed
        for t in range(0, 80):
            TEMP = _rotateLeft(A, 5) + f[t/20] + E + W[t] + K[t/20]
            E = D
            D = C
            C = _rotateLeft(B, 30) & 0xffffffff
            B = A
            A = TEMP & 0xffffffff
        """

        for t in range(0, 20):
            TEMP = _rotateLeft(A, 5) + ((B & C) | ((~ B) & D)) + E + W[t] + K[0]
            E = D
            D = C
            C = _rotateLeft(B, 30) & 0xffffffff
            B = A
            A = TEMP & 0xffffffff

        for t in range(20, 40):
            TEMP = _rotateLeft(A, 5) + (B ^ C ^ D) + E + W[t] + K[1]
            E = D
            D = C
            C = _rotateLeft(B, 30) & 0xffffffff
            B = A
            A = TEMP & 0xffffffff

        for t in range(40, 60):
            TEMP = _rotateLeft(A, 5) + ((B & C) | (B & D) | (C & D)) + E + W[t] + K[2]
            E = D
            D = C
            C = _rotateLeft(B, 30) & 0xffffffff
            B = A
            A = TEMP & 0xffffffff

        for t in range(60, 80):
            TEMP = _rotateLeft(A, 5) + (B ^ C ^ D)  + E + W[t] + K[3]
            E = D
            D = C
            C = _rotateLeft(B, 30) & 0xffffffff
            B = A
            A = TEMP & 0xffffffff


        self.H0 = (self.H0 + A) & 0xffffffff
        self.H1 = (self.H1 + B) & 0xffffffff
        self.H2 = (self.H2 + C) & 0xffffffff
        self.H3 = (self.H3 + D) & 0xffffffff
        self.H4 = (self.H4 + E) & 0xffffffff