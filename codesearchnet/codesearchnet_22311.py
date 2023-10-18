def load_gitconfig(self):
        """
        try use gitconfig info.
        author,email etc.
        """
        gitconfig_path = os.path.expanduser('~/.gitconfig')

        if os.path.exists(gitconfig_path):
            parser = Parser()
            parser.read(gitconfig_path)
            parser.sections()
            return parser

        pass