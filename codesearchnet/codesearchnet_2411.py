def MoveCursorToMyCenter(self, simulateMove: bool = True) -> tuple:
        """
        Move cursor to control's center.
        Return tuple, two ints tuple(x,y), the cursor positon relative to screen(0,0) after moving .
        """
        return self.MoveCursorToInnerPos(simulateMove=simulateMove)