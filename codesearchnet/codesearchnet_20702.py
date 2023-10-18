def transform(self):
        """Check the field values in self.dcmf1 and self.dcmf2 and returns True
        if all the field values are the same, False otherwise.

        Returns
        -------
        bool
        """
        if self.dcmf1 is None or self.dcmf2 is None:
            return np.inf

        for field_name in self.field_weights:
            if (str(getattr(self.dcmf1, field_name, ''))
                    != str(getattr(self.dcmf2, field_name, ''))):
                return False

        return True