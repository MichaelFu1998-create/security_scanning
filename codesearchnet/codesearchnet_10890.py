def hash(self):
        """Return an hash string computed on the PSF data."""
        hash_list = []
        for key, value in sorted(self.__dict__.items()):
            if not callable(value):
                if isinstance(value, np.ndarray):
                    hash_list.append(value.tostring())
                else:
                    hash_list.append(str(value))
        return hashlib.md5(repr(hash_list).encode()).hexdigest()