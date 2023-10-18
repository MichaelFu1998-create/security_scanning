def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(JqueryMediaMixin, self).media

        js = []

        if JQUERY_URL:
            js.append(JQUERY_URL)
        elif JQUERY_URL is not False:
            vendor = '' if django.VERSION < (1, 9, 0) else 'vendor/jquery/'
            extra = '' if settings.DEBUG else '.min'

            jquery_paths = [
                '{}jquery{}.js'.format(vendor, extra),
                'jquery.init.js',
            ]

            if USE_DJANGO_JQUERY:
                jquery_paths = ['admin/js/{}'.format(path) for path in jquery_paths]

            js.extend(jquery_paths)

        media += Media(js=js)
        return media