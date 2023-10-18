def raw_read(self):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """
        contents = b''
        with self.raw_iter() as filelike:
            for chunk in filelike:
                contents += chunk
        return contents