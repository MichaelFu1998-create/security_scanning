def mod2md(module, title, title_api_section, toc=True, maxdepth=0):
    """
    Generate markdown document from module, including API section.
    """
    docstr = module.__doc__

    text = doctrim(docstr)
    lines = text.split('\n')

    sections = find_sections(lines)
    if sections:
        level = min(n for n,t in sections) - 1
    else:
        level = 1

    api_md = []
    api_sec = []
    if title_api_section and module.__all__:
        sections.append((level+1, title_api_section))
        for name in module.__all__:
            api_sec.append((level+2, "`" + name + "`"))
            api_md += ['', '']
            entry = module.__dict__[name]
            if entry.__doc__:
                md, sec = doc2md(entry.__doc__, "`" + name + "`",
                        min_level=level+2, more_info=True, toc=False)
                api_sec += sec
                api_md += md

    sections += api_sec

    # headline
    head = next((i for i, l in enumerate(lines) if is_heading(l)), 0)
    md = [
        make_heading(level, title),
        "",
    ] + lines[:head]

    # main sections
    if toc:
        md += make_toc(sections, maxdepth)
        md += ['']
    md += _doc2md(lines[head:])

    # API section
    md += [
        '',
        '',
        make_heading(level+1, title_api_section),
    ]
    if toc:
        md += ['']
        md += make_toc(api_sec, 1)
    md += api_md

    return "\n".join(md)