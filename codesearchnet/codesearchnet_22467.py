def _call_proc(self,
                   proc: Callable[[Optional[str], Optional[str], argparse.Namespace], bool],
                   ifn: Optional[str],
                   ofn: Optional[str]) -> bool:
        """ Call the actual processor and intercept anything that goes wrong
        :param proc: Process to call
        :param ifn: Input file name to process.  If absent, typical use is stdin
        :param ofn: Output file name. If absent, typical use is stdout
        :return: true means process was successful
        """
        rslt = False
        try:
            rslt = proc(ifn, ofn, self.opts)
        except Exception as e:
            self._proc_error(ifn, e)
        return True if rslt or rslt is None else False