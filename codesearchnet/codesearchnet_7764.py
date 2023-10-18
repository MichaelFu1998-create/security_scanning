def zip(self):
        """Make a ZIP archive with all media files and return its path.

        If the ``zip_gallery`` setting is set,it contains the location of a zip
        archive with all original images of the corresponding directory.

        """
        zip_gallery = self.settings['zip_gallery']

        if zip_gallery and len(self) > 0:
            zip_gallery = zip_gallery.format(album=self)
            archive_path = join(self.dst_path, zip_gallery)
            if (self.settings.get('zip_skip_if_exists', False) and
                    isfile(archive_path)):
                self.logger.debug("Archive %s already created, passing",
                                  archive_path)
                return zip_gallery

            archive = zipfile.ZipFile(archive_path, 'w', allowZip64=True)
            attr = ('src_path' if self.settings['zip_media_format'] == 'orig'
                    else 'dst_path')

            for p in self:
                path = getattr(p, attr)
                try:
                    archive.write(path, os.path.split(path)[1])
                except OSError as e:
                    self.logger.warn('Failed to add %s to the ZIP: %s', p, e)

            archive.close()
            self.logger.debug('Created ZIP archive %s', archive_path)
            return zip_gallery