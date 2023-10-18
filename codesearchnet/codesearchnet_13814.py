def do_set(self, line):
        """
        Set a variable.
        """
        try:
            name, value = [part.strip() for part in line.split('=')]
            if name not in self.bot._vars:
                self.print_response('No such variable %s enter vars to see available vars' % name)
                return
            variable = self.bot._vars[name]
            variable.value = variable.sanitize(value.strip(';'))

            success, msg = self.bot.canvas.sink.var_changed(name, variable.value)
            if success:
                print('{}={}'.format(name, variable.value), file=self.stdout)
            else:
                print('{}\n'.format(msg), file=self.stdout)
        except Exception as e:
            print('Invalid Syntax.', e)
            return