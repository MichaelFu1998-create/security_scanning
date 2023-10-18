def retype_file(src, pyi_dir, targets, *, quiet=False, hg=False):
    """Retype `src`, finding types in `pyi_dir`. Save in `targets`.

    The file should remain formatted exactly as it was before, save for:
    - annotations
    - additional imports needed to satisfy annotations
    - additional module-level names needed to satisfy annotations

    Type comments in sources are normalized to type annotations.
    """
    with tokenize.open(src) as src_buffer:
        src_encoding = src_buffer.encoding
        src_node = lib2to3_parse(src_buffer.read())
    try:
        with open((pyi_dir / src.name).with_suffix('.pyi')) as pyi_file:
            pyi_txt = pyi_file.read()
    except FileNotFoundError:
        if not quiet:
            print(
                f'warning: .pyi file for source {src} not found in {pyi_dir}',
                file=sys.stderr,
            )
    else:
        pyi_ast = ast3.parse(pyi_txt)
        assert isinstance(pyi_ast, ast3.Module)
        reapply_all(pyi_ast.body, src_node)
    fix_remaining_type_comments(src_node)
    targets.mkdir(parents=True, exist_ok=True)
    with open(targets / src.name, 'w', encoding=src_encoding) as target_file:
        target_file.write(lib2to3_unparse(src_node, hg=hg))
    return targets / src.name