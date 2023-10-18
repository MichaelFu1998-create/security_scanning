def onesided_gen(self):
        """Return the one-sided frequency range as a generator.

        If :attr:`N` is even, the length is N/2 + 1.
        If :attr:`N` is odd, the length is (N+1)/2.

        ::

            >>> print(list(Range(8).onesided()))
            [0.0, 0.125, 0.25, 0.375, 0.5]
            >>> print(list(Range(9).onesided()))
            [0.0, 0.1111, 0.2222, 0.3333, 0.4444]

        """
        if self.N % 2 == 0:
            for n in range(0, self.N//2 + 1):
                yield n * self.df
        else:
            for n in range(0, (self.N+1)//2):
                yield n * self.df