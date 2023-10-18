def walk(self, **kwargs):
        """ Like `os.walk` and taking the same keyword arguments,
            but generating paths relative to the root.

            Starts in the fileset's root and filters based on its patterns.
            If ``with_root=True`` is passed in, the generated paths include
            the root path.
        """
        lead = ''
        if 'with_root' in kwargs and kwargs.pop('with_root'):
            lead = self.root.rstrip(os.sep) + os.sep

        for base, dirs, files in os.walk(self.root, **kwargs):
            prefix = base[len(self.root):].lstrip(os.sep)
            bits = prefix.split(os.sep) if prefix else []

            for dirname in dirs[:]:
                path = '/'.join(bits + [dirname])
                inclusive = self.included(path, is_dir=True)
                if inclusive:
                    yield lead + path + '/'
                elif inclusive is False:
                    dirs.remove(dirname)

            for filename in files:
                path = '/'.join(bits + [filename])
                if self.included(path):
                    yield lead + path