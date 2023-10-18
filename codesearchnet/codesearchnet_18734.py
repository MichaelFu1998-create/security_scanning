def run(self, raw_args):
        """parse and import the script, and then run the script's main function"""
        parser = self.parser
        args, kwargs = parser.parse_callback_args(raw_args)

        callback = kwargs.pop("main_callback")
        if parser.has_injected_quiet():
            levels = kwargs.pop("quiet_inject", "")
            logging.inject_quiet(levels)

        try:
            ret_code = callback(*args, **kwargs)
            ret_code = int(ret_code) if ret_code else 0

        except ArgError as e:
            # https://hg.python.org/cpython/file/2.7/Lib/argparse.py#l2374
            echo.err("{}: error: {}", parser.prog, str(e))
            ret_code = 2

        return ret_code