def is_isomorphic_to(self, other):
        """
        Returns true if other field's meta data (everything except value)
        is same as this one
        """
        return (isinstance(other, self.__class__)
                and self.field_type == other.field_type
                and self.field_id == other.field_id)