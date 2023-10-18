def GetSiblingControl(self, condition: Callable, forward: bool = True) -> 'Control':
        """
        Find a SiblingControl by condition(control: Control)->bool.
        forward: bool, if True, only search next siblings, if False, search pervious siblings first, then search next siblings.
        condition: Callable, function (control: Control)->bool.
        Return `Control` subclass or None.
        """
        if not forward:
            prev = self
            while True:
                prev = prev.GetPreviousSiblingControl()
                if prev:
                    if condition(prev):
                        return prev
                else:
                    break
        next_ = self
        while True:
            next_ = next_.GetNextSiblingControl()
            if next_:
                if condition(next_):
                    return next_
            else:
                break