def fetch(self, url, path, filename):
        """Verify if the file is already downloaded and complete. If they don't
        exists or if are not complete, use homura download function to fetch
        files. Return a list with the path of the downloaded file and the size
        of the remote file.
        """
        logger.debug('initializing download in ', url)
        remote_file_size = self.get_remote_file_size(url)

        if exists(join(path, filename)):
            size = getsize(join(path, filename))
            if size == remote_file_size:
                logger.error('%s already exists on your system' % filename)
                print('%s already exists on your system' % filename)
                return [join(path, filename), size]

        logger.debug('Downloading: %s' % filename)
        print('Downloading: %s' % filename)
        fetch(url, path)
        print('stored at %s' % path)
        logger.debug('stored at %s' % path)
        return [join(path, filename), remote_file_size]