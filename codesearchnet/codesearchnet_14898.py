def on_new(self):
        """
        Add a new empty code editor to the tab widget
        """
        interpreter, pyserver, args = self._get_backend_parameters()
        self.setup_editor(self.tabWidget.create_new_document(
            extension='.py', interpreter=interpreter, server_script=pyserver,
            args=args))
        self.actionRun.setDisabled(True)
        self.actionConfigure_run.setDisabled(True)