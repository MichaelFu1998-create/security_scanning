def run_3to2(args=None):
    """Convert Python files using lib3to2."""
    args = BASE_ARGS_3TO2 if args is None else BASE_ARGS_3TO2 + args
    try:
        proc = subprocess.Popen(['3to2'] + args, stderr=subprocess.PIPE)
    except OSError:
        for path in glob.glob('*.egg'):
            if os.path.isdir(path) and path not in sys.path:
                sys.path.append(path)
        try:
            from lib3to2.main import main as lib3to2_main
        except ImportError:
            raise OSError('3to2 script is unavailable.')
        else:
            if lib3to2_main('lib3to2.fixes', args):
                raise Exception('lib3to2 parsing error')
    else:
        # HACK: workaround for 3to2 never returning non-zero
        # when using the -j option.
        num_errors = 0
        while proc.poll() is None:
            line = proc.stderr.readline()
            sys.stderr.write(line)
            num_errors += line.count(': ParseError: ')
        if proc.returncode or num_errors:
            raise Exception('lib3to2 parsing error')