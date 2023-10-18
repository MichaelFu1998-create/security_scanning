def Hi(self, str_, salt, i):
        """The Hi(str, salt, i) function."""
        # pylint: disable=C0103
        Uj = self.HMAC(str_, salt + b"\000\000\000\001") # U1
        result = Uj
        for _ in range(2, i + 1):
            Uj = self.HMAC(str_, Uj)               # Uj = HMAC(str, Uj-1)
            result = self.XOR(result,  Uj)         # ... XOR Uj-1 XOR Uj
        return result