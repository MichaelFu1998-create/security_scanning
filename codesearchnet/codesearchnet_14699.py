def file_format(self):
        """Formats device filesystem"""
        log.info('Formating, can take minutes depending on flash size...')
        res = self.__exchange('file.format()', timeout=300)
        if 'format done' not in res:
            log.error(res)
        else:
            log.info(res)
        return res