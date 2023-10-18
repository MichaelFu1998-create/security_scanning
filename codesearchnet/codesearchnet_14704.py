def file_remove(self, path):
        """Removes a file on the device"""
        log.info('Remove '+path)
        cmd = 'file.remove("%s")' % path
        res = self.__exchange(cmd)
        log.info(res)
        return res