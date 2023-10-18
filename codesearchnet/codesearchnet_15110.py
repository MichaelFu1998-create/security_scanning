def string(self, string):
        """Load an object from a string and return the processed JSON content

        :return: the result of the processing step
        :param str string: the string to load the JSON from
        """
        object_ = json.loads(string)
        return self.object(object_)