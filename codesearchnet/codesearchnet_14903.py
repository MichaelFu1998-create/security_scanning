def on_current_tab_changed(self):
        """
        Update action states when the current tab changed.
        """
        self.menuEdit.clear()
        self.menuModes.clear()
        self.menuPanels.clear()
        editor = self.tabWidget.current_widget()
        self.menuEdit.setEnabled(editor is not None)
        self.menuModes.setEnabled(editor is not None)
        self.menuPanels.setEnabled(editor is not None)
        self.actionSave.setEnabled(editor is not None)
        self.actionSave_as.setEnabled(editor is not None)
        self.actionConfigure_run.setEnabled(editor is not None)
        self.actionRun.setEnabled(editor is not None)
        if editor is not None:
            self.setup_mnu_edit(editor)
            self.setup_mnu_modes(editor)
            self.setup_mnu_panels(editor)
        self.widgetOutline.set_editor(editor)
        self._update_status_bar(editor)