def begin(self):
        """begin

        """
        if self.isopen: return
        self.dropbox.open()
        self.isopen = True