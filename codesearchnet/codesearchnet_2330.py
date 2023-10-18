def Log(log: Any = '', consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        """
        t = datetime.datetime.now()
        frame = sys._getframe(1)
        log = '{}-{:02}-{:02} {:02}:{:02}:{:02}.{:03} Function: {}, Line: {} -> {}\n'.format(t.year, t.month, t.day,
            t.hour, t.minute, t.second, t.microsecond // 1000, frame.f_code.co_name, frame.f_lineno, log)
        Logger.Write(log, consoleColor, writeToFile, printToStdout, logFile)