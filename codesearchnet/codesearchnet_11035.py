def resize(self, width, height):
        """
        Pyqt specific resize callback.
        """
        if not self.fbo:
            return

        # pyqt reports sizes in actual buffer size
        self.width = width // self.widget.devicePixelRatio()
        self.height = height // self.widget.devicePixelRatio()
        self.buffer_width = width
        self.buffer_height = height

        super().resize(width, height)