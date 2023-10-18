def save(self, filename,  metadata={}, **data):
        """
        The implementation in the base class simply checks there is no
        clash between the metadata and data keys.
        """
        intersection = set(metadata.keys()) & set(data.keys())
        if intersection:
            msg = 'Key(s) overlap between data and metadata: %s'
            raise Exception(msg  % ','.join(intersection))