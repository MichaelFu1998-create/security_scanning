def MetroClose(self, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        Only work on Windows 8/8.1, if current window is Metro UI.
        waitTime: float.
        """
        if self.ClassName == METRO_WINDOW_CLASS_NAME:
            screenWidth, screenHeight = GetScreenSize()
            MoveTo(screenWidth // 2, 0, waitTime=0)
            DragDrop(screenWidth // 2, 0, screenWidth // 2, screenHeight, waitTime=waitTime)
        else:
            Logger.WriteLine('Window is not Metro!', ConsoleColor.Yellow)