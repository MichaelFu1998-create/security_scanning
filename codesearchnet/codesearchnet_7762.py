def thumbnail(self):
        """Path to the thumbnail of the album."""

        if self._thumbnail:
            # stop if it is already set
            return self._thumbnail

        # Test the thumbnail from the Markdown file.
        thumbnail = self.meta.get('thumbnail', [''])[0]

        if thumbnail and isfile(join(self.src_path, thumbnail)):
            self._thumbnail = url_from_path(join(
                self.name, get_thumb(self.settings, thumbnail)))
            self.logger.debug("Thumbnail for %r : %s", self, self._thumbnail)
            return self._thumbnail
        else:
            # find and return the first landscape image
            for f in self.medias:
                ext = splitext(f.filename)[1]
                if ext.lower() in self.settings['img_extensions']:
                    # Use f.size if available as it is quicker (in cache), but
                    # fallback to the size of src_path if dst_path is missing
                    size = f.size
                    if size is None:
                        size = get_size(f.src_path)

                    if size['width'] > size['height']:
                        self._thumbnail = (url_quote(self.name) + '/' +
                                           f.thumbnail)
                        self.logger.debug(
                            "Use 1st landscape image as thumbnail for %r : %s",
                            self, self._thumbnail)
                        return self._thumbnail

            # else simply return the 1st media file
            if not self._thumbnail and self.medias:
                for media in self.medias:
                    if media.thumbnail is not None:
                        self._thumbnail = (url_quote(self.name) + '/' +
                                           media.thumbnail)
                        break
                else:
                    self.logger.warning("No thumbnail found for %r", self)
                    return None

                self.logger.debug("Use the 1st image as thumbnail for %r : %s",
                                  self, self._thumbnail)
                return self._thumbnail

            # use the thumbnail of their sub-directories
            if not self._thumbnail:
                for path, album in self.gallery.get_albums(self.path):
                    if album.thumbnail:
                        self._thumbnail = (url_quote(self.name) + '/' +
                                           album.thumbnail)
                        self.logger.debug(
                            "Using thumbnail from sub-directory for %r : %s",
                            self, self._thumbnail)
                        return self._thumbnail

        self.logger.error('Thumbnail not found for %r', self)
        return None