def id_to_object(self, line):
        """
            Resolves an ip adres to a range object, creating it if it doesn't exists.
        """
        result = Range.get(line, ignore=404)
        if not result:
            result = Range(range=line)
            result.save()
        return result