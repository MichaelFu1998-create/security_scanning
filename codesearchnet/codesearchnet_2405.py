def GetChildren(self) -> list:
        """
        Return list, a list of `Control` subclasses.
        """
        children = []
        child = self.GetFirstChildControl()
        while child:
            children.append(child)
            child = child.GetNextSiblingControl()
        return children