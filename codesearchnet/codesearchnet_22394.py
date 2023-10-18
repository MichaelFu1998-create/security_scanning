def get_json_tuples(self, prettyprint=False, translate=True):
        """
        Get the data as JSON tuples
        """
        j = self.get_json(prettyprint, translate)
        if len(j) > 2:
            if prettyprint:
                j = j[1:-2] + ",\n"
            else:
                j = j[1:-1] + ","
        else:
            j = ""
        return j