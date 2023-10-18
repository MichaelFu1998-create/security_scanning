def help(self, long=False):
        """Print help; same as using ``?`` in ``ipython``. long=True also gives call signature."""
        print("\ncommand: {0!s}\n\n".format(self.command_name))
        print(self.__doc__)
        if long:
            print("\ncall method: command():\n")
            print(self.__call__.__doc__)