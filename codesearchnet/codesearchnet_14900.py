def on_save_as(self):
        """
        Save the current editor document as.
        """
        path = self.tabWidget.current_widget().file.path
        path = os.path.dirname(path) if path else ''
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save', path)
        if filename:
            self.tabWidget.save_current(filename)
            self.recent_files_manager.open_file(filename)
            self.menu_recents.update_actions()
            self.actionRun.setEnabled(True)
            self.actionConfigure_run.setEnabled(True)
            self._update_status_bar(self.tabWidget.current_widget())