def url(self):
        """
        The URL to access this preview.
        """
        return reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': self.module,
            'preview': type(self).__name__,
        })