def get_urls(self):
        """Add URLs needed to handle image uploads."""
        urls = patterns(
            '',
            url(r'^upload/$', self.admin_site.admin_view(self.handle_upload), name='quill-file-upload'),
        )
        return urls + super(QuillAdmin, self).get_urls()