def reverse_id(self):
        """Generate the id of reverse_variable from the reaction's id."""
        return '_'.join((self.id, 'reverse',
                         hashlib.md5(
                             self.id.encode('utf-8')).hexdigest()[0:5]))