def Move(self, unit: int, count: int, waitTime: float = OPERATION_WAIT_TIME) -> int:
        """
        Call IUIAutomationTextRange::Move.
        Move the text range forward or backward by the specified number of text units.
        unit: int, a value in class `TextUnit`.
        count: int, the number of text units to move.
               A positive value moves the text range forward.
               A negative value moves the text range backward. Zero has no effect.
        waitTime: float.
        Return: int, the number of text units actually moved.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-move
        """
        ret = self.textRange.Move(unit, count)
        time.sleep(waitTime)
        return ret