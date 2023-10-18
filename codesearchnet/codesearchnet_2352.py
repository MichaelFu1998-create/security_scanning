def FindItemByProperty(control: 'Control', propertyId: int, propertyValue) -> 'Control':
        """
        Call IUIAutomationItemContainerPattern::FindItemByProperty.
        control: `Control` or its subclass.
        propertyValue: COM VARIANT according to propertyId? todo.
        propertyId: int, a value in class `PropertyId`.
        Return `Control` subclass, a control within a containing element, based on a specified property value.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationitemcontainerpattern-finditembyproperty
        """
        ele = self.pattern.FindItemByProperty(control.Element, propertyId, propertyValue)
        return Control.CreateControlFromElement(ele)