def run():
    """Run compiler
    """
    aparse = argparse.ArgumentParser(
        description='LessCss Compiler', epilog='<< jtm@robot.is @_o >>')
    aparse.add_argument(
        '-v', '--version', action='version', version=VERSION_STR)
    aparse.add_argument(
        '-I',
        '--include',
        action="store",
        type=str,
        help="Included less-files (comma separated)")
    aparse.add_argument(
        '-V',
        '--verbose',
        action="store_true",
        default=False,
        help="Verbose mode")
    aparse.add_argument(
        '-C',
        '--dont_create_dirs',
        action="store_true",
        default=False,
        help="Creates directories when outputing files (lessc non-compatible)")
    fgroup = aparse.add_argument_group('Formatting options')
    fgroup.add_argument(
        '-x',
        '--minify',
        action="store_true",
        default=False,
        help="Minify output")
    fgroup.add_argument(
        '-X',
        '--xminify',
        action="store_true",
        default=False,
        help="Minify output, no end of block newlines")
    fgroup.add_argument('-t', '--tabs', help="Use tabs", action="store_true")
    fgroup.add_argument(
        '-s',
        '--spaces',
        help="Number of startline spaces (default 2)",
        default=2)
    dgroup = aparse.add_argument_group(
        'Directory options', 'Compiles all *.less files in directory that '
        'have a newer timestamp than it\'s css file.')
    dgroup.add_argument('-o', '--out', action="store", help="Output directory")
    dgroup.add_argument(
        '-r',
        '--recurse',
        action="store_true",
        help="Recursive into subdirectorys")
    dgroup.add_argument(
        '-f',
        '--force',
        action="store_true",
        help="Force recompile on all files")
    dgroup.add_argument(
        '-m',
        '--min-ending',
        action="store_true",
        default=False,
        help="Add '.min' into output filename. eg, name.min.css")
    dgroup.add_argument(
        '-D',
        '--dry-run',
        action="store_true",
        default=False,
        help="Dry run, do not write files")
    group = aparse.add_argument_group('Debugging')
    group.add_argument(
        '-g',
        '--debug',
        action="store_true",
        default=False,
        help="Debugging information")
    group.add_argument(
        '-S',
        '--scopemap',
        action="store_true",
        default=False,
        help="Scopemap")
    group.add_argument(
        '-L',
        '--lex-only',
        action="store_true",
        default=False,
        help="Run lexer on target")
    group.add_argument(
        '-N',
        '--no-css',
        action="store_true",
        default=False,
        help="No css output")
    aparse.add_argument('target', help="less file or directory")
    aparse.add_argument('output', nargs='?', help="output file path")
    args = aparse.parse_args()
    try:
        #
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #
        if args.lex_only:
            lex = lexer.LessLexer()
            ll = lex.file(args.target)
            while True:
                tok = ll.token()
                if not tok:
                    break
                if hasattr(tok,
                           "lexer"):  # literals don't have the lexer attribute
                    print(tok, "State:", tok.lexer.lexstate)
                else:
                    print(tok)
            print('EOF')
            sys.exit()
        #
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #
        yacctab = 'yacctab' if args.debug else None
        scope = None
        if args.include:
            for u in args.include.split(','):
                if os.path.exists(u):
                    p = parser.LessParser(
                        yacc_debug=(args.debug),
                        lex_optimize=True,
                        yacc_optimize=(not args.debug),
                        tabfile=yacctab,
                        verbose=args.verbose)
                    p.parse(filename=u, debuglevel=args.debug)
                    if not scope:
                        scope = p.scope
                    else:
                        scope.update(p.scope)
                else:
                    sys.exit('included file `%s` not found ...' % u)
                sys.stdout.flush()
        p = None
        f = formatter.Formatter(args)
        if not os.path.exists(args.target):
            sys.exit("Target not found '%s' ..." % args.target)
        if os.path.isdir(args.target):
            ldirectory(args.target, args.out, args, scope)
            if args.dry_run:
                print('Dry run, nothing done.', file=sys.stderr)
        else:
            p = parser.LessParser(
                yacc_debug=(args.debug),
                lex_optimize=True,
                yacc_optimize=(not args.debug),
                scope=copy.deepcopy(scope),
                verbose=args.verbose)
            p.parse(filename=args.target, debuglevel=args.debug)
            if args.scopemap:
                args.no_css = True
                p.scopemap()
            if not args.no_css and p:
                out = f.format(p)
                if args.output:
                    if not args.dont_create_dirs and not os.path.exists(
                            os.path.dirname(args.output)):
                        try:
                            os.makedirs(os.path.dirname(args.output))
                        except OSError as exc:  # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    with open(args.output, "w") as f:
                        f.write(out)
                else:
                    print(out)
    except (KeyboardInterrupt, SystemExit, IOError):
        sys.exit('\nAborting...')