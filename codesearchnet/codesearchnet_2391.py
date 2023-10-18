def BoundingRectangle(self) -> Rect:
        """
        Property BoundingRectangle.
        Call IUIAutomationElement::get_CurrentBoundingRectangle.
        Return `Rect`.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentboundingrectangle

        rect = control.BoundingRectangle
        print(rect.left, rect.top, rect.right, rect.bottom, rect.width(), rect.height(), rect.xcenter(), rect.ycenter())
        """
        rect = self.Element.CurrentBoundingRectangle
        return Rect(rect.left, rect.top, rect.right, rect.bottom)