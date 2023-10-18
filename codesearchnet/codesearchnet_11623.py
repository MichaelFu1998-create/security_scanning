def publish(self, registry=None):
        ''' Publish to the appropriate registry, return a description of any
            errors that occured, or None if successful.
            No VCS tagging is performed.
        '''
        if (registry is None) or (registry == registry_access.Registry_Base_URL):
            if 'private' in self.description and self.description['private']:
                return "this %s is private and cannot be published" % (self.description_filename.split('.')[0])
        upload_archive = os.path.join(self.path, 'upload.tar.gz')
        fsutils.rmF(upload_archive)
        fd = os.open(upload_archive, os.O_CREAT | os.O_EXCL | os.O_RDWR | getattr(os, "O_BINARY", 0))
        with os.fdopen(fd, 'rb+') as tar_file:
            tar_file.truncate()
            self.generateTarball(tar_file)
            logger.debug('generated tar file of length %s', tar_file.tell())
            tar_file.seek(0)
            # calculate the hash of the file before we upload it:
            shasum = hashlib.sha256()
            while True:
                chunk = tar_file.read(1000)
                if not chunk:
                    break
                shasum.update(chunk)
            logger.debug('generated tar file has hash %s', shasum.hexdigest())
            tar_file.seek(0)
            with self.findAndOpenReadme() as readme_file_wrapper:
                if not readme_file_wrapper:
                    logger.warning("no readme.md file detected")
                with open(self.getDescriptionFile(), 'r') as description_file:
                    return registry_access.publish(
                        self.getRegistryNamespace(),
                        self.getName(),
                        self.getVersion(),
                        description_file,
                        tar_file,
                        readme_file_wrapper.file,
                        readme_file_wrapper.extension().lower(),
                        registry=registry
                    )