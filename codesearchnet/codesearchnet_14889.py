def setPlainText(self, txt, mimetype='text/x-python', encoding='utf-8'):
        """
        Extends QCodeEdit.setPlainText to allow user to setPlainText without
        mimetype (since the python syntax highlighter does not use it).
        """
        try:
            self.syntax_highlighter.docstrings[:] = []
            self.syntax_highlighter.import_statements[:] = []
        except AttributeError:
            pass
        super(PyCodeEditBase, self).setPlainText(txt, mimetype, encoding)