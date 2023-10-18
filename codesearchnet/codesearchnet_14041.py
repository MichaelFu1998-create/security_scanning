def hide_variables_window(self):
        """
        Hide the variables window
        """
        if self.var_window is not None:
            self.var_window.window.destroy()
            self.var_window = None