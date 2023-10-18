def exec_file(self, path):
        """execute the lines in the local file 'path'"""
        filename = os.path.basename(path)
        log.info('Execute %s', filename)

        content = from_file(path).replace('\r', '').split('\n')

        res = '> '
        for line in content:
            line = line.rstrip('\n')
            retlines = (res + self.__exchange(line)).splitlines()
            # Log all but the last line
            res = retlines.pop()
            for lin in retlines:
                log.info(lin)
        # last line
        log.info(res)