def parse(self, args):
        """
        :param args: arguments
        :type args: None or string or list of string
        :return: formatted arguments if specified else ``self.default_args``
        :rtype: list of string
        """
        if args is None:
            args = self._default_args
        if isinstance(args, six.string_types):
            args = shlex.split(args)
        return args