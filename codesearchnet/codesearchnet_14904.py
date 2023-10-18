def on_run(self):
        """
        Run the current current script
        """
        filename = self.tabWidget.current_widget().file.path
        wd = os.path.dirname(filename)
        args = Settings().get_run_config_for_file(filename)
        self.interactiveConsole.start_process(
            Settings().interpreter, args=[filename] + args, cwd=wd)
        self.dockWidget.show()
        self.actionRun.setEnabled(False)
        self.actionConfigure_run.setEnabled(False)