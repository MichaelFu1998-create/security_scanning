def get_pipe(self, object_type):
        """
            Returns a generator that maps the input of the pipe to an elasticsearch object.
            Will call id_to_object if it cannot serialize the data from json.
        """
        for line in sys.stdin:
            try:
                data = json.loads(line.strip())
                obj = object_type(**data)
                yield obj
            except ValueError:
                yield self.id_to_object(line.strip())