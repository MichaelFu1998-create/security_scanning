def find_out_attribs(self):
        """
        Get all out attributes in the shader source.

        :return: List of attribute names
        """
        names = []
        for line in self.lines:
            if line.strip().startswith("out "):
                names.append(line.split()[2].replace(';', ''))
        return names