def decode_file_args(self, argv: List[str]) -> List[str]:
        """
        Preprocess any arguments that begin with the fromfile prefix char(s).
        This replaces the one in Argparse because it
            a) doesn't process "-x y" correctly and
            b) ignores bad files
        :param argv: raw options list
        :return: options list with file references replaced
        """
        for arg in [arg for arg in argv if arg[0] in self.fromfile_prefix_chars]:
            argv.remove(arg)
            with open(arg[1:]) as config_file:
                argv += shlex.split(config_file.read())
                return self.decode_file_args(argv)
        return argv