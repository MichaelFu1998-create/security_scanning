def _dump_to_file(self, file):
        """dump to the file"""
        xmltodict.unparse(self.object(), file, pretty=True)