def clearForm(self):
        """Clear all form fields (except author)."""
        
        self.logui.titleEntry.clear()
        self.logui.textEntry.clear()

        # Remove all log selection menus except the first
        while self.logMenuCount > 1:
            self.removeLogbook(self.logMenus[-1])