def make_toc(sections, maxdepth=0):
    """
    Generate table of contents for array of section names.
    """
    if not sections:
        return []
    outer = min(n for n,t in sections)
    refs = []
    for ind,sec in sections:
        if maxdepth and ind-outer+1 > maxdepth:
            continue
        ref = sec.lower()
        ref = ref.replace('`', '')
        ref = ref.replace(' ', '-')
        ref = ref.replace('?', '')
        refs.append("    "*(ind-outer) + "- [%s](#%s)" % (sec, ref))
    return refs