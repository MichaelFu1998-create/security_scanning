def write_file_to_package_zip(self, filename, src_filename):
        """
        Writes a local file in to the zip file and adds it to the manifest
        dictionary

        :param filename: The zip file name

        :param src_filename: the local file name
        """
        f = open(src_filename)
        with f:
            data = f.read()
        self.manifest[filename] = md5hash(data)
        self.package_zip.write(src_filename, filename)