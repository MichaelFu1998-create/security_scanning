def on_goto_out_of_doc(self, assignment):
        """
        Open the a new tab when goto goes out of the current document.

        :param assignment: Destination
        """
        editor = self.open_file(assignment.module_path)
        if editor:
            TextHelper(editor).goto_line(assignment.line, assignment.column)