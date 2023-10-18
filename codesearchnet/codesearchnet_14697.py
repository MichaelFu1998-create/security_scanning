def file_list(self):
        """list files on the device"""
        log.info('Listing files')
        res = self.__exchange(LIST_FILES)
        res = res.split('\r\n')
        # skip first and last lines
        res = res[1:-1]
        files = []
        for line in res:
            files.append(line.split('\t'))
        return files