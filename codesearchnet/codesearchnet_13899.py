def _mmult(self, a, b):
        """ Returns the 3x3 matrix multiplication of A and B.
            Note that scale(), translate(), rotate() work with premultiplication,
            e.g. the matrix A followed by B = BA and not AB.
        """
        # No need to optimize (C version is just as fast).
        return [
            a[0] * b[0] + a[1] * b[3],
            a[0] * b[1] + a[1] * b[4],
            0,
            a[3] * b[0] + a[4] * b[3],
            a[3] * b[1] + a[4] * b[4],
            0,
            a[6] * b[0] + a[7] * b[3] + b[6],
            a[6] * b[1] + a[7] * b[4] + b[7],
            1
        ]