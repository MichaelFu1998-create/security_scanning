def parse_and_process_args(self, args):
        """Handle the parsing of command line arguments."""

        parser = argparse.ArgumentParser(
            prog="python -m rflint",
            description="A style checker for robot framework plain text files.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog = (
                "You can use 'all' in place of RULENAME to refer to all rules. \n"
                "\n"
                "For example: '--ignore all --warn DuplicateTestNames' will ignore all\n"
                "rules except DuplicateTestNames.\n"
                "\n"
                "FORMAT is a string that performs a substitution on the following \n"
                "patterns: {severity}, {linenumber}, {char}, {message}, and {rulename}.\n"
                "\n"
                "For example: --format 'line: {linenumber}: message: {message}'. \n"
                "\n"
                "ARGUMENTFILE is a filename with contents that match the format of \n"
                "standard robot framework argument files\n"
                "\n"
                "If you give a directory as an argument, all files in the directory\n"
                "with the suffix .txt, .robot or .tsv will be processed. With the \n"
                "--recursive option, subfolders within the directory will also be\n"
                "processed."
                )
            )
        parser.add_argument("--error", "-e", metavar="RULENAME", action=SetErrorAction,
                            help="Assign a severity of ERROR to the given RULENAME")
        parser.add_argument("--ignore", "-i", metavar="RULENAME", action=SetIgnoreAction,
                            help="Ignore the given RULENAME")
        parser.add_argument("--warning", "-w", metavar="RULENAME", action=SetWarningAction,
                            help="Assign a severity of WARNING for the given RULENAME")
        parser.add_argument("--list", "-l", action="store_true",
                            help="show a list of known rules and exit")
        parser.add_argument("--describe", "-d", action="store_true",
                            help="describe the given rules")
        parser.add_argument("--no-filenames", action="store_false", dest="print_filenames", 
                            default=True,
                            help="suppress the printing of filenames")
        parser.add_argument("--format", "-f", 
                            help="Define the output format",
                            default='{severity}: {linenumber}, {char}: {message} ({rulename})')
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("--verbose", "-v", action="store_true", default=False,
                            help="Give verbose output")
        parser.add_argument("--configure", "-c", action=ConfigureAction,
                            help="Configure a rule")
        parser.add_argument("--recursive", "-r", action="store_true", default=False,
                            help="Recursively scan subfolders in a directory")
        parser.add_argument("--rulefile", "-R", action=RulefileAction,
                            help="import additional rules from the given RULEFILE")
        parser.add_argument("--argumentfile", "-A", action=ArgfileLoader,
                            help="read arguments from the given file")
        parser.add_argument('args', metavar="file", nargs=argparse.REMAINDER)

        # create a custom namespace, in which we can store a reference to
        # our rules. This lets the custom argument actions access the list
        # of rules
        ns = argparse.Namespace()
        setattr(ns, "app", self)
        args = parser.parse_args(args, ns)

        Rule.output_format = args.format

        return args