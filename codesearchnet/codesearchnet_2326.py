def Write(log: Any, consoleColor: int = ConsoleColor.Default, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None, printTruncateLen: int = 0) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        printTruncateLen: int, if <= 0, log is not truncated when print.
        """
        if not isinstance(log, str):
            log = str(log)
        if printToStdout and sys.stdout:
            isValidColor = (consoleColor >= ConsoleColor.Black and consoleColor <= ConsoleColor.White)
            if isValidColor:
                SetConsoleColor(consoleColor)
            try:
                if printTruncateLen > 0 and len(log) > printTruncateLen:
                    sys.stdout.write(log[:printTruncateLen] + '...')
                else:
                    sys.stdout.write(log)
            except Exception as ex:
                SetConsoleColor(ConsoleColor.Red)
                isValidColor = True
                sys.stdout.write(ex.__class__.__name__ + ': can\'t print the log!')
                if log.endswith('\n'):
                    sys.stdout.write('\n')
            if isValidColor:
                ResetConsoleColor()
            sys.stdout.flush()
        if not writeToFile:
            return
        fileName = logFile if logFile else Logger.FileName
        try:
            fout = open(fileName, 'a+', encoding='utf-8')
            fout.write(log)
        except Exception as ex:
            if sys.stdout:
                sys.stdout.write(ex.__class__.__name__ + ': can\'t write the log!')
        finally:
            if fout:
                fout.close()