def _CompareFunction(self, control: 'Control', depth: int) -> bool:
        """
        Define how to search.
        control: `Control` or its subclass.
        depth: int, tree depth from searchFromControl.
        Return bool.
        """
        for key, value in self.searchProperties.items():
            if 'ControlType' == key:
                if value != control.ControlType:
                    return False
            elif 'ClassName' == key:
                if value != control.ClassName:
                    return False
            elif 'AutomationId' == key:
                if value != control.AutomationId:
                    return False
            elif 'Name' == key:
                if value != control.Name:
                    return False
            elif 'SubName' == key:
                if value not in control.Name:
                    return False
            elif 'RegexName' == key:
                if not self.regexName.match(control.Name):
                    return False
            elif 'Depth' == key:
                if value != depth:
                    return False
            elif 'Compare' == key:
                if not value(control, depth):
                    return False
        return True