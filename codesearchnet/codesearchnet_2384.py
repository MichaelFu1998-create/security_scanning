def ZoomByUnit(self, zoomUnit: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTransformPattern2::ZoomByUnit.
        Zoom the viewport of the control by the specified unit.
        zoomUnit: int, a value in class `ZoomUnit`.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern2-zoombyunit
        """
        ret = self.pattern.ZoomByUnit(zoomUnit) == S_OK
        time.sleep(waitTime)
        return ret