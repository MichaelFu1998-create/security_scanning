def _launch_all(self, launchers):
        """
        Launches all available launchers.
        """
        for launcher in launchers:
            print("== Launching  %s ==" % launcher.batch_name)
            launcher()
        return True