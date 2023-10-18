def MoveEndpointByUnit(self, endPoint: int, unit: int, count: int, waitTime: float = OPERATION_WAIT_TIME) -> int:
        """
        Call IUIAutomationTextRange::MoveEndpointByUnit.
        Move one endpoint of the text range the specified number of text units within the document range.
        endPoint: int, a value in class `TextPatternRangeEndpoint`.
        unit: int, a value in class `TextUnit`.
        count: int, the number of units to move.
                    A positive count moves the endpoint forward.
                    A negative count moves backward.
                    A count of 0 has no effect.
        waitTime: float.
        Return int, the count of units actually moved.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-moveendpointbyunit
        """
        ret = self.textRange.MoveEndpointByUnit(endPoint, unit, count)
        time.sleep(waitTime)
        return ret