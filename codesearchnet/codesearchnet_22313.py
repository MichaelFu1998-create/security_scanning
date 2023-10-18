def add_arguments(cls):
        """
        Init project.
        """
        return [
            (('--yes',), dict(action='store_true', help='clean .git repo')),
            (('--variable', '-s'),
             dict(nargs='+', help='set extra variable,format is name:value')),
            (('--skip-builtin',),
             dict(action='store_true', help='skip replace builtin variable')),
        ]