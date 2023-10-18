def _generate_index(self):
        """rebuild the _dict index"""
        self._dict = {v.id: k for k, v in enumerate(self)}