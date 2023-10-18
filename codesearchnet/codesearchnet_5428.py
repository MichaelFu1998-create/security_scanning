def write_to_package_zip(self, filename, data):
        """
        Writes data to the zip file and adds it to the manifest dictionary

        :param filename: The zip file name

        :param data: the data
        """
        self.manifest[filename] = md5hash(data)
        self.package_zip.writestr(filename, data)