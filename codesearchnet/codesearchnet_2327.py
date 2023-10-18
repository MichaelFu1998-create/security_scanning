def WriteLine(log: Any, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        """
        Logger.Write('{}\n'.format(log), consoleColor, writeToFile, printToStdout, logFile)