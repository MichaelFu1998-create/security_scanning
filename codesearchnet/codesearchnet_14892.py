def mousePressEvent(self, e):
        """
        Emits open_file_requested if the press event occured  over
        a file location string.
        """
        super(PyInteractiveConsole, self).mousePressEvent(e)
        cursor = self.cursorForPosition(e.pos())
        p = cursor.positionInBlock()
        usd = cursor.block().userData()
        if usd and usd.start_pos_in_block <= p <= usd.end_pos_in_block:
            if e.button() == QtCore.Qt.LeftButton:
                self.open_file_requested.emit(usd.filename, usd.line)