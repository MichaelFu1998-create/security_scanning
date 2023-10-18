def patch_anchors(parser, show_progressbar):
    """
    Consume ``ParseEntry``s then patch docs for TOCs by calling
    *parser*'s ``find_and_patch_entry``.
    """
    files = defaultdict(list)
    try:
        while True:
            pentry = (yield)
            try:
                fname, anchor = pentry.path.split("#")
                files[fname].append(
                    TOCEntry(name=pentry.name, type=pentry.type, anchor=anchor)
                )
            except ValueError:
                # pydoctor has no anchors for e.g. classes
                pass
    except GeneratorExit:
        pass

    def patch_files(files):
        for fname, entries in files:
            full_path = os.path.join(parser.doc_path, fname)
            with codecs.open(full_path, mode="r", encoding="utf-8") as fp:
                soup = BeautifulSoup(fp, "html.parser")
                for entry in entries:
                    if not parser.find_and_patch_entry(soup, entry):
                        log.debug(
                            "Can't find anchor {} in {}.".format(
                                entry.anchor, click.format_filename(fname)
                            )
                        )
            with open(full_path, mode="wb") as fp:
                fp.write(soup.encode("utf-8"))

    if show_progressbar is True:
        with click.progressbar(
            files.items(),
            width=0,
            length=len(files),
            label="Adding table of contents meta data...",
        ) as pbar:
            patch_files(pbar)
    else:
        patch_files(files.items())