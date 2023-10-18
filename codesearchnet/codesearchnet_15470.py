def ldirectory(inpath, outpath, args, scope):
    """Compile all *.less files in directory
    Args:
        inpath (str): Path to compile
        outpath (str): Output directory
        args (object): Argparse Object
        scope (Scope): Scope object or None
    """
    yacctab = 'yacctab' if args.debug else None
    if not outpath:
        sys.exit("Compile directory option needs -o ...")
    else:
        if not os.path.isdir(outpath):
            if args.verbose:
                print("Creating '%s'" % outpath, file=sys.stderr)
            if not args.dry_run:
                os.mkdir(outpath)
    less = glob.glob(os.path.join(inpath, '*.less'))
    f = formatter.Formatter(args)
    for lf in less:
        outf = os.path.splitext(os.path.basename(lf))
        minx = '.min' if args.min_ending else ''
        outf = "%s/%s%s.css" % (outpath, outf[0], minx)
        if not args.force and os.path.exists(outf):
            recompile = os.path.getmtime(outf) < os.path.getmtime(lf)
        else:
            recompile = True
        if recompile:
            print('%s -> %s' % (lf, outf))
            p = parser.LessParser(
                yacc_debug=(args.debug),
                lex_optimize=True,
                yacc_optimize=(not args.debug),
                scope=scope,
                tabfile=yacctab,
                verbose=args.verbose)
            p.parse(filename=lf, debuglevel=0)
            css = f.format(p)
            if not args.dry_run:
                with open(outf, 'w') as outfile:
                    outfile.write(css)
        elif args.verbose:
            print('skipping %s, not modified' % lf, file=sys.stderr)
        sys.stdout.flush()
    if args.recurse:
        [
            ldirectory(
                os.path.join(inpath, name), os.path.join(outpath, name), args,
                scope) for name in os.listdir(inpath)
            if os.path.isdir(os.path.join(inpath, name))
            and not name.startswith('.') and not name == outpath
        ]