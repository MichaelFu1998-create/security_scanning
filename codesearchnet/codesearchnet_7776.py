def generate_context(self, album):
        """Generate the context dict for the given path."""

        from . import __url__ as sigal_link
        self.logger.info("Output album : %r", album)
        return {
            'album': album,
            'index_title': self.index_title,
            'settings': self.settings,
            'sigal_link': sigal_link,
            'theme': {'name': os.path.basename(self.theme),
                      'url': url_from_path(os.path.relpath(self.theme_path,
                                                           album.dst_path))},
        }