def _parse_options(self, argv, location):
        """Parse the options part of an argument list.
        IN:
        lsArgs <list str>:
            List of arguments. Will be altered.
        location <str>:
            A user friendly string describing where this data came from.
            
        """
        observed = []
        while argv:
            if argv[0].startswith('--'):
                name = argv.pop(0)[2:]
                # '--' means end of options.
                if not name:
                    break
                if name not in self.options:
                    raise InvalidOption(name)
                option = self.options[name]
                if not option.recurring:
                    if option in observed:
                        raise OptionRecurrenceError(name)
                    observed.append(option)
                option.parse(argv, name, location)
            elif argv[0].startswith('-'):
                # A single - is not an abbreviation block, but the first positional arg.
                if argv[0] == '-':
                    break
                block = argv.pop(0)[1:]
                # Abbrevs for options that take values go last in the block.
                for abbreviation in block[:-1]:
                    if self.abbreviations[abbreviation].nargs != 0:
                        raise BadAbbreviationBlock(abbreviation, block, "options that require value arguments must be last in abbreviation blocks")
                # Parse individual options.
                for abbreviation in block:
                    option = self.abbreviations[abbreviation]
                    if not option.recurring:
                        if option in observed:
                            raise OptionRecurrenceError(option.name)
                        observed.append(option)
                    option.parse(argv, '-' + abbreviation, location)
            # only arguments that start with -- or - can be Options.
            else:
                break