def trigger_fullscreen_action(self, fullscreen):
        """
        Toggle fullscreen from outside the GUI,
        causes the GUI to updated and run all its actions.
        """
        action = self.action_group.get_action('fullscreen')
        action.set_active(fullscreen)