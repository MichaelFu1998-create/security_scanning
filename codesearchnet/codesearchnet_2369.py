def GetBoundingRectangles(self) -> list:
        """
        Call IUIAutomationTextRange::GetBoundingRectangles.
        textAttributeId: int, a value in class `TextAttributeId`.
        Return list, a list of `Rect`.
            bounding rectangles for each fully or partially visible line of text in a text range..
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getboundingrectangles

        for rect in textRange.GetBoundingRectangles():
            print(rect.left, rect.top, rect.right, rect.bottom, rect.width(), rect.height(), rect.xcenter(), rect.ycenter())
        """
        floats = self.textRange.GetBoundingRectangles()
        rects = []
        for i in range(len(floats) // 4):
            rect = Rect(int(floats[i * 4]), int(floats[i * 4 + 1]),
                                        int(floats[i * 4]) + int(floats[i * 4 + 2]), int(floats[i * 4 + 1]) + int(floats[i * 4 + 3]))
            rects.append(rect)
        return rects