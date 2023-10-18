def file_contains(self, *args, **kwargs):
        """
        filename text
        http://docs.fabfile.org/en/1.13/api/contrib/files.html#fabric.contrib.files.contains
        """
        from fabric.contrib.files import contains
        return contains(*args, **kwargs)