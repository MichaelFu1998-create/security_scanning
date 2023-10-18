def setup_actions(self):
        """ Connects slots to signals """
        self.actionOpen.triggered.connect(self.on_open)
        self.actionNew.triggered.connect(self.on_new)
        self.actionSave.triggered.connect(self.on_save)
        self.actionSave_as.triggered.connect(self.on_save_as)
        self.actionQuit.triggered.connect(
            QtWidgets.QApplication.instance().quit)
        self.tabWidget.current_changed.connect(self.on_current_tab_changed)
        self.tabWidget.last_tab_closed.connect(self.on_last_tab_closed)
        self.actionAbout.triggered.connect(self.on_about)
        self.actionRun.triggered.connect(self.on_run)
        self.interactiveConsole.process_finished.connect(
            self.on_process_finished)
        self.actionConfigure_run.triggered.connect(self.on_configure_run)