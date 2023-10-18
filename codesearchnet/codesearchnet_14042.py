def var_window_closed(self, widget):
        """
        Called if user clicked close button on var window
        :param widget:
        :return:
        """
        # TODO - Clean up the menu handling stuff its a bit spagetti right now
        self.action_group.get_action('vars').set_active(False)
        self.show_vars = False
        self.var_window = None