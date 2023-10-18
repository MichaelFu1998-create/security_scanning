def setup_editor(self, editor):
        """
        Setup the python editor, run the server and connect a few signals.

        :param editor: editor to setup.
        """
        editor.cursorPositionChanged.connect(self.on_cursor_pos_changed)
        try:
            m = editor.modes.get(modes.GoToAssignmentsMode)
        except KeyError:
            pass
        else:
            assert isinstance(m, modes.GoToAssignmentsMode)
            m.out_of_doc.connect(self.on_goto_out_of_doc)