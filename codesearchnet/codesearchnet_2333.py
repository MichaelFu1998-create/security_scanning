def FromControl(self, control: 'Control', x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> bool:
        """
        Capture a control to Bitmap.
        control: `Control` or its subclass.
        x: int.
        y: int.
        width: int.
        height: int.
        x, y: the point in control's internal position(from 0,0)
        width, height: image's width and height from x, y, use 0 for entire area,
        If width(or height) < 0, image size will be control's width(or height) - width(or height).
        Return bool, True if succeed otherwise False.
        """
        rect = control.BoundingRectangle
        while rect.width() == 0 or rect.height() == 0:
            #some controls maybe visible but their BoundingRectangle are all 0, capture its parent util valid
            control = control.GetParentControl()
            if not control:
                return False
            rect = control.BoundingRectangle
        if width <= 0:
            width = rect.width() + width
        if height <= 0:
            height = rect.height() + height
        handle = control.NativeWindowHandle
        if handle:
            left = x
            top = y
            right = left + width
            bottom = top + height
        else:
            while True:
                control = control.GetParentControl()
                handle = control.NativeWindowHandle
                if handle:
                    pRect = control.BoundingRectangle
                    left = rect.left - pRect.left + x
                    top = rect.top - pRect.top + y
                    right = left + width
                    bottom = top + height
                    break
        return self.FromHandle(handle, left, top, right, bottom)