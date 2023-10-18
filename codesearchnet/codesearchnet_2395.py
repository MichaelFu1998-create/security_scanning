def GetPropertyValueEx(self, propertyId: int, ignoreDefaultValue: int) -> Any:
        """
        Call IUIAutomationElement::GetCurrentPropertyValueEx.
        propertyId: int, a value in class `PropertyId`.
        ignoreDefaultValue: int, 0 or 1.
        Return Any, corresponding type according to propertyId.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalueex
        """
        return self.Element.GetCurrentPropertyValueEx(propertyId, ignoreDefaultValue)