def is_isomorphic_to(self, other):
        """
        Returns true if all fields of other struct are isomorphic to this
        struct's fields
        """
        return (isinstance(other, self.__class__)
                and
                len(self.fields) == len(other.fields)
                and
                all(a.is_isomorphic_to(b) for a, b in zip(self.fields,
                                                          other.fields)))