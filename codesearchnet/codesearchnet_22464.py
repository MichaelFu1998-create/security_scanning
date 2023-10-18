def _parser_exit(parser: argparse.ArgumentParser, proc: "DirectoryListProcessor", _=0,
                 message: Optional[str]=None) -> None:
    """
    Override the default exit in the parser.
    :param parser:
    :param _: exit code.  Unused because we don't exit
    :param message: Optional message
    """
    if message:
        parser._print_message(message, sys.stderr)
    proc.successful_parse = False