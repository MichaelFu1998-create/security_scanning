def ColorfullyWriteLine(log: str, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: str.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.

        ColorfullyWriteLine('Hello <Color=Green>Green</Color> !!!'), color name must be in Logger.ColorNames.
        """
        Logger.ColorfullyWrite(log + '\n', consoleColor, writeToFile, printToStdout, logFile)