def file_do(self, filename):
        """Execute a file on the device using 'do'"""
        log.info('Executing '+filename)
        res = self.__exchange('dofile("'+filename+'")')
        log.info(res)
        return res