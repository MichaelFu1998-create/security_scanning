def popUpItem(self, *args):
        """Return the specified item in a pop up menu."""
        self.Press()
        time.sleep(.5)
        return self._menuItem(self, *args)