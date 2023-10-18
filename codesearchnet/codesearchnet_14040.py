def show_variables_window(self):
        """
        Show the variables window.
        """
        if self.var_window is None and self.bot._vars:
            self.var_window = VarWindow(self, self.bot, '%s variables' % (self.title or 'Shoebot'))
            self.var_window.window.connect("destroy", self.var_window_closed)