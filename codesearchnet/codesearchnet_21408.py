def get_pipe(self):
        """
            Returns a list that maps the input of the pipe to an elasticsearch object.
            Will call id_to_object if it cannot serialize the data from json.
        """
        lines = []
        for line in sys.stdin:
            try:
                lines.append(self.line_to_object(line.strip()))
            except ValueError:
                pass
            except KeyError:
                pass
        return lines