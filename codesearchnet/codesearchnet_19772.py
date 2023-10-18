def getTableOfContents(self):
        """
        This function populates the internal tableOfContents list with the contents
        of the zip file TOC. If the server does not support ranged requests, this will raise
        and exception. It will also throw an exception if the TOC cannot be found.
        """

        self.directory_size = self.getDirectorySize()
        if self.directory_size > 65536:
            self.directory_size += 2
            self.requestContentDirectory()


        # and find the offset from start of file where it can be found
        directory_start = unpack("i", self.raw_bytes[self.directory_end + 16: self.directory_end + 20])[0]

        # find the data in the raw_bytes
        self.raw_bytes = self.raw_bytes
        current_start = directory_start - self.start
        filestart = 0
        compressedsize = 0
        tableOfContents = []

        try:
            while True:
                # get file name size (n), extra len (m) and comm len (k)
                zip_n = unpack("H", self.raw_bytes[current_start + 28: current_start + 28 + 2])[0]
                zip_m = unpack("H", self.raw_bytes[current_start + 30: current_start + 30 + 2])[0]
                zip_k = unpack("H", self.raw_bytes[current_start + 32: current_start + 32 + 2])[0]

                filename = self.raw_bytes[current_start + 46: current_start + 46 + zip_n]

                # check if this is the index file
                filestart = unpack("I", self.raw_bytes[current_start + 42: current_start + 42 + 4])[0]
                compressedsize = unpack("I", self.raw_bytes[current_start + 20: current_start + 20 + 4])[0]
                uncompressedsize = unpack("I", self.raw_bytes[current_start + 24: current_start + 24 + 4])[0]
                tableItem = {
                    'filename': filename,
                    'compressedsize': compressedsize,
                    'uncompressedsize': uncompressedsize,
                    'filestart': filestart
                }
                tableOfContents.append(tableItem)

                # not this file, move along
                current_start = current_start + 46 + zip_n + zip_m + zip_k
        except:
            pass

        self.tableOfContents = tableOfContents
        return tableOfContents