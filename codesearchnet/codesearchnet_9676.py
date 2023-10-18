def doc2md(docstr, title, min_level=1, more_info=False, toc=True, maxdepth=0):
    """
    Convert a docstring to a markdown text.
    """
    text = doctrim(docstr)
    lines = text.split('\n')

    sections = find_sections(lines)
    if sections:
        level = min(n for n,t in sections) - 1
    else:
        level = 1

    shiftlevel = 0
    if level < min_level:
        shiftlevel = min_level - level
        level = min_level
        sections = [(lev+shiftlevel, tit) for lev,tit in sections]

    head = next((i for i, l in enumerate(lines) if is_heading(l)), 0)
    md = [
        make_heading(level, title),
        "",
    ] + lines[:head]
    if toc:
        md += make_toc(sections, maxdepth)
        md += ['']
    md += _doc2md(lines[head:], shiftlevel)
    if more_info:
        return (md, sections)
    else:
        return "\n".join(md)