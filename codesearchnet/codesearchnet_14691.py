def verify_file(self, path, destination, verify='none'):
        """Tries to verify if path has same checksum as destination.
            Valid options for verify is 'raw', 'sha1' or 'none'
        """
        content = from_file(path)
        log.info('Verifying using %s...' % verify)
        if verify == 'raw':

            data = self.download_file(destination)
            if content != data:
                log.error('Raw verification failed.')
                raise VerificationError('Verification failed.')
            else:
                log.info('Verification successful. Contents are identical.')
        elif verify == 'sha1':
            #Calculate SHA1 on remote file. Extract just hash from result
            data = self.__exchange('shafile("'+destination+'")').splitlines()[1]
            log.info('Remote SHA1: %s', data)

            #Calculate hash of local data
            filehashhex = hashlib.sha1(content.encode(ENCODING)).hexdigest()
            log.info('Local SHA1: %s', filehashhex)
            if data != filehashhex:
                log.error('SHA1 verification failed.')
                raise VerificationError('SHA1 Verification failed.')
            else:
                log.info('Verification successful. Checksums match')

        elif verify != 'none':
            raise Exception(verify + ' is not a valid verification method.')