def write(self, album, media_group):
        ''' Generate the media page and save it '''

        from sigal import __url__ as sigal_link
        file_path = os.path.join(album.dst_path, media_group[0].filename)

        page = self.template.render({
            'album': album,
            'media': media_group[0],
            'previous_media': media_group[-1],
            'next_media': media_group[1],
            'index_title': self.index_title,
            'settings': self.settings,
            'sigal_link': sigal_link,
            'theme': {'name': os.path.basename(self.theme),
                      'url': url_from_path(os.path.relpath(self.theme_path,
                                                           album.dst_path))},
        })

        output_file = "%s.html" % file_path

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page)