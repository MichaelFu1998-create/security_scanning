def MoveEndpointByRange(self, srcEndPoint: int, textRange: 'TextRange', targetEndPoint: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTextRange::MoveEndpointByRange.
        Move one endpoint of the current text range to the specified endpoint of a second text range.
        srcEndPoint: int, a value in class `TextPatternRangeEndpoint`.
        textRange: `TextRange`.
        targetEndPoint: int, a value in class `TextPatternRangeEndpoint`.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-moveendpointbyrange
        """
        ret = self.textRange.MoveEndpointByRange(srcEndPoint, textRange.textRange, targetEndPoint) == S_OK
        time.sleep(waitTime)
        return ret