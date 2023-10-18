def process(self):
        """ Calls the external cleanser scripts to (optionally) purge the meta data and then
            send the contents of the dropbox via email.
        """

        if self.num_attachments > 0:
            self.status = u'100 processor running'
            fs_dirty_archive = self._create_backup()
            # calling _process_attachments has the side-effect of updating `send_attachments`
            self._process_attachments()
            if self.status_int < 500 and not self.send_attachments:
                    self._create_archive()

        if self.status_int >= 500 and self.status_int < 600:
            # cleansing failed
            # if configured, we need to move the uncleansed archive to
            # the appropriate folder and notify the editors
            if 'dropbox_dirty_archive_url_format' in self.settings:
                # create_archive
                shutil.move(
                    fs_dirty_archive,
                    '%s/%s.zip.pgp' % (self.container.fs_archive_dirty, self.drop_id))
                # update status
                # it's now considered 'successful-ish' again
                self.status = '490 cleanser failure but notify success'

        if self.status_int == 800:
            # at least one attachment was not supported
            # if configured, we need to move the uncleansed archive to
            # the appropriate folder and notify the editors
            if 'dropbox_dirty_archive_url_format' in self.settings:
                # create_archive
                shutil.move(
                    fs_dirty_archive,
                    '%s/%s.zip.pgp' % (self.container.fs_archive_dirty, self.drop_id))

        if self.status_int < 500 or self.status_int == 800:
            try:
                if self._notify_editors() > 0:
                    if self.status_int < 500:
                        self.status = '900 success'
                else:
                    self.status = '605 smtp failure'
            except Exception:
                import traceback
                tb = traceback.format_exc()
                self.status = '610 smtp error (%s)' % tb

        self.cleanup()
        return self.status