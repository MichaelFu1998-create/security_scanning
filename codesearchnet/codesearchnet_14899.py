def on_open(self):
        """
        Shows an open file dialog and open the file if the dialog was
        accepted.

        """
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open')
        if filename:
            self.open_file(filename)
        self.actionRun.setEnabled(True)
        self.actionConfigure_run.setEnabled(True)