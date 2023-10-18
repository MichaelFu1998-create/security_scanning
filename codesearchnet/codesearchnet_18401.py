def launch(self,
               argv=None,
               showusageonnoargs=False,
               width=0,
               helphint="Use with --help for more information.\n",
               debug_parser=False):
        """Do the usual stuff to initiallize the program.
        
        Read config files and parse arguments, and if the user has used any 
        of the help/version/settings options, display help and exit.
        
        If debug_parser is false, don't catch ParseErrors and exit with user
        friendly help. Crash with traceback instead.
        
        configfiles is a list of config files. None means use self.configfiles.
        
        sections is a list of configfile section names to read. None means use
        self.sections.
        
        argv is a list of arguments to parse. Will be modified. None means use
        copy of sys.argv. argv[0] is ignored.
        
        If showusageonnoargs is true, show usage and exit if the user didn't 
        give any args. Should be False if there are no required PositionalArgs.
        
        width is the maximum allowed page width. 0 means use self.width.
        
        helphint is a string that hints on how to get more help which is 
        displayed at the end of usage help messages. 
        """
        if showusageonnoargs and len(argv) == 1:
            print self.shorthelp(width=width)
            if helphint:
                print self._wrap(helphint, indent=2, width=width)
            sys.exit(0)
        parsing_error = None
        try:
            self.parse_files()
            self.parse_argv(argv)
        except ParseError, parsing_error:
            if debug_parser:
                raise
        for optiontype in ['help', 'longhelp', 'settings', 'version']:
            name = self.basic_option_names.get(optiontype)
            if name and self[name]:
                methodname = optiontype.rstrip('help') + 'help'
                print getattr(self, methodname)(width)
                sys.exit()
        if parsing_error:
            self.graceful_exit(parsing_error, width)