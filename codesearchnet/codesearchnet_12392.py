def main(
    source,
    force,
    name,
    quiet,
    verbose,
    destination,
    add_to_dash,
    add_to_global,
    icon,
    index_page,
    enable_js,
    online_redirect_url,
    parser,
):
    """
    Convert docs from SOURCE to Dash.app's docset format.
    """
    try:
        logging.config.dictConfig(
            create_log_config(verbose=verbose, quiet=quiet)
        )
    except ValueError as e:
        click.secho(e.args[0], fg="red")
        raise SystemExit(1)

    if icon:
        icon_data = icon.read()
        if not icon_data.startswith(PNG_HEADER):
            log.error(
                '"{}" is not a valid PNG image.'.format(
                    click.format_filename(icon.name)
                )
            )
            raise SystemExit(1)
    else:
        icon_data = None

    source, dest, name = setup_paths(
        source,
        destination,
        name=name,
        add_to_global=add_to_global,
        force=force,
    )
    if parser is None:
        parser = parsers.get_doctype(source)
        if parser is None:
            log.error(
                '"{}" does not contain a known documentation format.'.format(
                    click.format_filename(source)
                )
            )
            raise SystemExit(errno.EINVAL)
    docset = prepare_docset(
        source, dest, name, index_page, enable_js, online_redirect_url
    )
    doc_parser = parser(doc_path=docset.docs)
    log.info(
        (
            "Converting "
            + click.style("{parser_name}", bold=True)
            + ' docs from "{src}" to "{dst}".'
        ).format(
            parser_name=parser.name,
            src=click.format_filename(source, shorten=True),
            dst=click.format_filename(dest),
        )
    )

    with docset.db_conn:
        log.info("Parsing documentation...")
        toc = patch_anchors(doc_parser, show_progressbar=not quiet)
        for entry in doc_parser.parse():
            docset.db_conn.execute(
                "INSERT INTO searchIndex VALUES (NULL, ?, ?, ?)",
                entry.as_tuple(),
            )
            toc.send(entry)
        count = docset.db_conn.execute(
            "SELECT COUNT(1) FROM searchIndex"
        ).fetchone()[0]
        log.info(
            (
                "Added "
                + click.style("{count:,}", fg="green" if count > 0 else "red")
                + " index entries."
            ).format(count=count)
        )
        toc.close()

    if icon_data:
        add_icon(icon_data, dest)

    if add_to_dash or add_to_global:
        log.info("Adding to Dash.app...")
        os.system('open -a dash "{}"'.format(dest))