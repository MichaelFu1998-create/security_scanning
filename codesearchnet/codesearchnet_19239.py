def registerGoodClass(self, class_):
        """
        Internal bookkeeping to handle nested classes
        """
        # Class itself added to "good" list
        self._valid_classes.append(class_)
        # Recurse into any inner classes
        for name, cls in class_members(class_):
            if self.isValidClass(cls):
                self.registerGoodClass(cls)