def create_subparsers(self, parser):
        """ get config for subparser and create commands"""
        subparsers = parser.add_subparsers()
        for name in self.config['subparsers']:
            subparser = subparsers.add_parser(name)
            self.create_commands(self.config['subparsers'][name], subparser)