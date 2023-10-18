def printdir(self):
        """Print a table of contents for the RAR file."""
        print("%-46s %19s %12s" % ("File Name", "Modified    ", "Size"))
        for rarinfo in self.filelist:
            date = "%d-%02d-%02d %02d:%02d:%02d" % rarinfo.date_time[:6]
            print("%-46s %s %12d" % (
                rarinfo.filename, date, rarinfo.file_size))