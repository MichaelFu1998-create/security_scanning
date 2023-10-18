def thumbnail(self):
        """Path to the thumbnail image (relative to the album directory)."""

        if not isfile(self.thumb_path):
            self.logger.debug('Generating thumbnail for %r', self)
            path = (self.dst_path if os.path.exists(self.dst_path)
                    else self.src_path)
            try:
                # if thumbnail is missing (if settings['make_thumbs'] is False)
                s = self.settings
                if self.type == 'image':
                    image.generate_thumbnail(
                        path, self.thumb_path, s['thumb_size'],
                        fit=s['thumb_fit'])
                elif self.type == 'video':
                    video.generate_thumbnail(
                        path, self.thumb_path, s['thumb_size'],
                        s['thumb_video_delay'], fit=s['thumb_fit'],
                        converter=s['video_converter'])
            except Exception as e:
                self.logger.error('Failed to generate thumbnail: %s', e)
                return
        return url_from_path(self.thumb_name)