def mouseMoveEvent(self, e):
        """
        Extends mouseMoveEvent to display a pointing hand cursor when the
        mouse cursor is over a file location
        """
        super(PyInteractiveConsole, self).mouseMoveEvent(e)
        cursor = self.cursorForPosition(e.pos())
        assert isinstance(cursor, QtGui.QTextCursor)
        p = cursor.positionInBlock()
        usd = cursor.block().userData()
        if usd and usd.start_pos_in_block <= p <= usd.end_pos_in_block:
            if QtWidgets.QApplication.overrideCursor() is None:
                QtWidgets.QApplication.setOverrideCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            if QtWidgets.QApplication.overrideCursor() is not None:
                QtWidgets.QApplication.restoreOverrideCursor()