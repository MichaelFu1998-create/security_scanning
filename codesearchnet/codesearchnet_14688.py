def download_file(self, filename):
        """Download a file from device to local filesystem"""
        res = self.__exchange('send("{filename}")'.format(filename=filename))
        if ('unexpected' in res) or ('stdin' in res):
            log.error('Unexpected error downloading file: %s', res)
            raise Exception('Unexpected error downloading file')

        #tell device we are ready to receive
        self.__write('C')
        #we should get a NUL terminated filename to start with
        sent_filename = self.__expect(NUL).strip()
        log.info('receiveing ' + sent_filename)

        #ACK to start download
        self.__write(ACK, True)
        buf = ''

        data = ''
        chunk, buf = self.__read_chunk(buf)
        #read chunks until we get an empty which is the end
        while chunk != '':
            self.__write(ACK, True)
            data = data + chunk
            chunk, buf = self.__read_chunk(buf)
        return data