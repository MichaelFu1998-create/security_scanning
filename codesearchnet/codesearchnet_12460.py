def retype_path(
    src, pyi_dir, targets, *, src_explicitly_given=False, quiet=False, hg=False
):
    """Recursively retype files or directories given. Generate errors."""
    if src.is_dir():
        for child in src.iterdir():
            if child == pyi_dir or child == targets:
                continue
            yield from retype_path(
                child, pyi_dir / src.name, targets / src.name, quiet=quiet, hg=hg,
            )
    elif src.suffix == '.py' or src_explicitly_given:
        try:
            retype_file(src, pyi_dir, targets, quiet=quiet, hg=hg)
        except Exception as e:
            yield (
                src,
                str(e),
                type(e),
                traceback.format_tb(e.__traceback__),
            )