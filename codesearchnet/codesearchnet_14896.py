def open_file(self, path, line=None):
        """
        Creates a new GenericCodeEdit, opens the requested file and adds it
        to the tab widget.

        :param path: Path of the file to open

        :return The opened editor if open succeeded.
        """
        editor = None
        if path:
            interpreter, pyserver, args = self._get_backend_parameters()
            editor = self.tabWidget.open_document(
                path, None, interpreter=interpreter, server_script=pyserver,
                args=args)
            if editor:
                self.setup_editor(editor)
            self.recent_files_manager.open_file(path)
            self.menu_recents.update_actions()
        if line is not None:
            TextHelper(self.tabWidget.current_widget()).goto_line(line)
        return editor