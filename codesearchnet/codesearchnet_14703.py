def file_compile(self, path):
        """Compiles a file specified by path on the device"""
        log.info('Compile '+path)
        cmd = 'node.compile("%s")' % path
        res = self.__exchange(cmd)
        log.info(res)
        return res