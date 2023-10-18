def add_variables(self):
        """
        Add all widgets to specified vbox
        :param container:
        :return:
        """
        for k, v in self.bot._vars.items():
            if not hasattr(v, 'type'):
                raise AttributeError(
                    '%s is not a Shoebot Variable - see https://shoebot.readthedocs.io/en/latest/commands.html#dynamic-variables' % k)
            self.add_variable(v)