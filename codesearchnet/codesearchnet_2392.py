def GetClickablePoint(self) -> tuple:
        """
        Call IUIAutomationElement::GetClickablePoint.
        Return tuple, (x: int, y: int, gotClickable: bool), like (20, 10, True)
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getclickablepoint
        """
        point, gotClickable = self.Element.GetClickablePoint()
        return (point.x, point.y, bool(gotClickable))