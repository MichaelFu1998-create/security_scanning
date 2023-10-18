def _proc_error(ifn: str, e: Exception) -> None:
        """ Report an error
        :param ifn: Input file name
        :param e: Exception to report
        """
        type_, value_, traceback_ = sys.exc_info()
        traceback.print_tb(traceback_, file=sys.stderr)
        print(file=sys.stderr)
        print("***** ERROR: %s" % ifn, file=sys.stderr)
        print(str(e), file=sys.stderr)