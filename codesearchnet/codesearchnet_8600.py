def to_representation(self, data):
        """
        This selectively calls to_representation on each result that was processed by create.
        """
        return [
            self.child.to_representation(item) if 'detail' in item else item for item in data
        ]