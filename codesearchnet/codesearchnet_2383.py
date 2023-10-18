def Zoom(self, zoomLevel: float, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTransformPattern2::Zoom.
        Zoom the viewport of the control.
        zoomLevel: float for int.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern2-zoom
        """
        ret = self.pattern.Zoom(zoomLevel) == S_OK
        time.sleep(waitTime)
        return ret