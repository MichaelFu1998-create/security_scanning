def main(src, pyi_dir, target_dir, incremental, quiet, replace_any, hg, traceback):
    """Re-apply type annotations from .pyi stubs to your codebase."""
    Config.incremental = incremental
    Config.replace_any = replace_any
    returncode = 0
    for src_entry in src:
        for file, error, exc_type, tb in retype_path(
            Path(src_entry),
            pyi_dir=Path(pyi_dir),
            targets=Path(target_dir),
            src_explicitly_given=True,
            quiet=quiet,
            hg=hg,
        ):
            print(f'error: {file}: {error}', file=sys.stderr)
            if traceback:
                print('Traceback (most recent call last):', file=sys.stderr)
                for line in tb:
                    print(line, file=sys.stderr, end='')
                print(f'{exc_type.__name__}: {error}', file=sys.stderr)
            returncode += 1
    if not src and not quiet:
        print('warning: no sources given', file=sys.stderr)

    # According to http://tldp.org/LDP/abs/html/index.html starting with 126
    # we have special returncodes.
    sys.exit(min(returncode, 125))