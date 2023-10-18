def GetAncestorControl(self, condition: Callable) -> 'Control':
        """
        Get a ancestor control that matches the condition.
        condition: Callable, function (control: Control, depth: int)->bool,
                   depth starts with -1 and decreses when search goes up.
        Return `Control` subclass or None.
        """
        ancestor = self
        depth = 0
        while True:
            ancestor = ancestor.GetParentControl()
            depth -= 1
            if ancestor:
                if condition(ancestor, depth):
                    return ancestor
            else:
                break