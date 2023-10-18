def _join_dirname(self, *args):
        """return os.path.join(os.path.dirname(args[0]), *args[1:])"""
        # extra function because I need to use it in a method that defines
        # the kwarg 'os', which collides with os.path...
        return os.path.join(os.path.dirname(args[0]), *args[1:])