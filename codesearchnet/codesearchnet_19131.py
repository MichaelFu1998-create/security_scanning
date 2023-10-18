def _get_Ks(self):
        "Ks as an array and type-checked."
        Ks = as_integer_type(self.Ks)
        if Ks.ndim != 1:
            raise TypeError("Ks should be 1-dim, got shape {}".format(Ks.shape))
        if Ks.min() < 1:
            raise ValueError("Ks should be positive; got {}".format(Ks.min()))
        return Ks