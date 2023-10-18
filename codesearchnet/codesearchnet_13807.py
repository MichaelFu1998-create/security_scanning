def do_vars(self, line):
        """
        List bot variables and values
        """
        if self.bot._vars:
            max_name_len = max([len(name) for name in self.bot._vars])
            for i, (name, v) in enumerate(self.bot._vars.items()):
                keep = i < len(self.bot._vars) - 1
                self.print_response("%s = %s" % (name.ljust(max_name_len), v.value), keep=keep)
        else:
            self.print_response("No vars")