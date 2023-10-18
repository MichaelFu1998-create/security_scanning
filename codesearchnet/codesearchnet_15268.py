def _create_archive(self):
        """ creates an encrypted archive of the dropbox outside of the drop directory.
        """
        self.status = u'270 creating final encrypted backup of cleansed attachments'
        return self._create_encrypted_zip(source='clean', fs_target_dir=self.container.fs_archive_cleansed)