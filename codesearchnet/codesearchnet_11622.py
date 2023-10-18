def generateTarball(self, file_object):
        ''' Write a tarball of the current component/target to the file object
            "file_object", which must already be open for writing at position 0
        '''
        archive_name = '%s-%s' % (self.getName(), self.getVersion())
        def filterArchive(tarinfo):
            if tarinfo.name.find(archive_name) == 0 :
                unprefixed_name = tarinfo.name[len(archive_name)+1:]
                tarinfo.mode &= 0o775
            else:
                unprefixed_name = tarinfo.name
            if self.ignores(unprefixed_name):
                return None
            else:
                return tarinfo
        with tarfile.open(fileobj=file_object, mode='w:gz') as tf:
            logger.info('generate archive extracting to "%s"' % archive_name)
            tf.add(self.path, arcname=archive_name, filter=filterArchive)