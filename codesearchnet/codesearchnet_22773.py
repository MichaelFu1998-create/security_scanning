def show_version(self):
        """ custom command line  action to show version """
        class ShowVersionAction(argparse.Action):
            def __init__(inner_self, nargs=0, **kw):
                super(ShowVersionAction, inner_self).__init__(nargs=nargs, **kw)

            def __call__(inner_self, parser, args, value, option_string=None):
                print("{parser_name} version: {version}".format(
                    parser_name=self.config.get(
                        "parser", {}).get("prog"),
                    version=self.prog_version))
        return ShowVersionAction