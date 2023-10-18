def do_toggle_variables(self, action):
        """
        Widget Action to toggle showing the variables window.
        """
        self.show_vars = action.get_active()
        if self.show_vars:
            self.show_variables_window()
        else:
            self.hide_variables_window()