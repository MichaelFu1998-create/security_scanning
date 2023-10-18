def parser(self):
        """return the parser for the current name"""
        module = self.module

        subcommands = self.subcommands
        if subcommands:
            module_desc = inspect.getdoc(module)
            parser = Parser(description=module_desc, module=module)
            subparsers = parser.add_subparsers()

            for sc_name, callback in subcommands.items():
                sc_name = sc_name.replace("_", "-")
                cb_desc = inspect.getdoc(callback)
                sc_parser = subparsers.add_parser(
                    sc_name,
                    callback=callback,
                    help=cb_desc
                )

        else:
            parser = Parser(callback=self.callbacks[self.function_name], module=module)

        return parser