def _create_encrypted_zip(self, source='dirty', fs_target_dir=None):
        """ creates a zip file from the drop and encrypts it to the editors.
        the encrypted archive is created inside fs_target_dir"""
        backup_recipients = [r for r in self.editors if checkRecipient(self.gpg_context, r)]

        # this will be handled by watchdog, no need to send for each drop
        if not backup_recipients:
            self.status = u'500 no valid keys at all'
            return self.status

        # calculate paths
        fs_backup = join(self.fs_path, '%s.zip' % source)
        if fs_target_dir is None:
            fs_backup_pgp = join(self.fs_path, '%s.zip.pgp' % source)
        else:
            fs_backup_pgp = join(fs_target_dir, '%s.zip.pgp' % self.drop_id)
        fs_source = dict(
            dirty=self.fs_dirty_attachments,
            clean=self.fs_cleansed_attachments
        )

        # create archive
        with ZipFile(fs_backup, 'w', ZIP_STORED) as backup:
            if exists(join(self.fs_path, 'message')):
                backup.write(join(self.fs_path, 'message'), arcname='message')
            for fs_attachment in fs_source[source]:
                backup.write(fs_attachment, arcname=split(fs_attachment)[-1])

        # encrypt archive
        with open(fs_backup, "rb") as backup:
            self.gpg_context.encrypt_file(
                backup,
                backup_recipients,
                always_trust=True,
                output=fs_backup_pgp
            )

        # cleanup
        remove(fs_backup)
        return fs_backup_pgp