def GetTopLevelControl(self) -> 'Control':
        """
        Get the top level control which current control lays.
        If current control is top level, return self.
        If current control is root control, return None.
        Return `PaneControl` or `WindowControl` or None.
        """
        handle = self.NativeWindowHandle
        if handle:
            topHandle = GetAncestor(handle, GAFlag.Root)
            if topHandle:
                if topHandle == handle:
                    return self
                else:
                    return ControlFromHandle(topHandle)
            else:
                #self is root control
                pass
        else:
            control = self
            while True:
                control = control.GetParentControl()
                handle = control.NativeWindowHandle
                if handle:
                    topHandle = GetAncestor(handle, GAFlag.Root)
                    return ControlFromHandle(topHandle)