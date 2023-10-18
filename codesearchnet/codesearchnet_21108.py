def write(self, fh, pretty=True):
        """
        API niceness defaulting to composite.write_json().
        """
        return self.write_json(fh, pretty=pretty)