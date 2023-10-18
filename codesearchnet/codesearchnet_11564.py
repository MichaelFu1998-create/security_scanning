def end(self):
        """end

        """
        if not self.isopen: return
        self.dropbox.close()
        self.isopen = False