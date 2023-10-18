def centerdc_gen(self):
        """Return the centered frequency range as a generator.

        ::

            >>> print(list(Range(8).centerdc_gen()))
            [-0.5, -0.375, -0.25, -0.125, 0.0, 0.125, 0.25, 0.375]

        """
        for a in range(0, self.N):
            yield (a-self.N/2) * self.df