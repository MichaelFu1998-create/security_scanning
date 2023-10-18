def setup_mnu_panels(self, editor):
        """
        Setup the panels menu for the current editor.
        :param editor:
        """
        for panel in editor.panels:
            if panel.dynamic:
                continue
            a = QtWidgets.QAction(self.menuModes)
            a.setText(panel.name)
            a.setCheckable(True)
            a.setChecked(panel.enabled)
            a.changed.connect(self.on_panel_state_changed)
            a.panel = weakref.proxy(panel)
            self.menuPanels.addAction(a)