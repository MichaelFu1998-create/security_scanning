def IsTopLevel(self) -> bool:
        """Determine whether current control is top level."""
        handle = self.NativeWindowHandle
        if handle:
            return GetAncestor(handle, GAFlag.Root) == handle
        return False