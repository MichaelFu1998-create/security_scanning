def CreateControlFromElement(element) -> 'Control':
        """
        Create a concreate `Control` from a com type `IUIAutomationElement`.
        element: `ctypes.POINTER(IUIAutomationElement)`.
        Return a subclass of `Control`, an instance of the control's real type.
        """
        if element:
            controlType = element.CurrentControlType
            if controlType in ControlConstructors:
                return ControlConstructors[controlType](element=element)
            else:
                Logger.WriteLine("element.CurrentControlType returns {}, invalid ControlType!".format(controlType), ConsoleColor.Red)