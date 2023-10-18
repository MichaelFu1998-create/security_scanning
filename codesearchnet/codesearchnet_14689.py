def read_file(self, filename, destination=''):
        """reading data from device into local file"""
        if not destination:
            destination = filename
        log.info('Transferring %s to %s', filename, destination)
        data = self.download_file(filename)

        # Just in case, the filename may contain folder, so create it if needed.
        log.info(destination)
        if not os.path.exists(os.path.dirname(destination)):
            try:
                os.makedirs(os.path.dirname(destination))
            except OSError as e:  # Guard against race condition
                if e.errno != errno.EEXIST:
                    raise
        with open(destination, 'w') as fil:
            fil.write(data)