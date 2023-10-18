def map(self, data):
        """Mapping part of string preparation."""
        result = []
        for char in data:
            ret = None
            for lookup in self.mapping:
                ret = lookup(char)
                if ret is not None:
                    break
            if ret is not None:
                result.append(ret)
            else:
                result.append(char)
        return result