def set_display_columns(self, set_true=[], set_false=[]):
        """Add or remove columns from the output."""
        for i in range(len(self.fields)):
            if self.fields[i].name in set_true:
                self.fields[i].display = True
            elif self.fields[i].name in set_false:
                self.fields[i].display = False