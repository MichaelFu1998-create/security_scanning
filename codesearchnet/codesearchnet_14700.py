def file_print(self, filename):
        """Prints a file on the device to console"""
        log.info('Printing ' + filename)
        res = self.__exchange(PRINT_FILE.format(filename=filename))
        log.info(res)
        return res