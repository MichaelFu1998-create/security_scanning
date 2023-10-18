def linspace(self, start, stop, n):
        """ Simple replacement for numpy linspace"""
        if n == 1: return [start]
        L = [0.0] * n
        nm1 = n - 1
        nm1inv = 1.0 / nm1
        for i in range(n):
            L[i] = nm1inv * (start*(nm1 - i) + stop*i)
        return L