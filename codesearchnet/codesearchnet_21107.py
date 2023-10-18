def write_json(self, fh, pretty=True):
        """
        Write composite object to file handle in JSON format.

        Args:
            fh (file): File handle to write to.
            pretty (bool): Sort keys and indent in output.
        """
        sjson = json.JSONEncoder().encode(self.json())
        if pretty:
            json.dump(json.loads(sjson), fh, sort_keys=True, indent=4)
        else:
            json.dump(json.loads(sjson), fh)
        return