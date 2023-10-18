def _f_gene(sid, prefix="G_"):
    """Clips gene prefix from id."""
    sid = sid.replace(SBML_DOT, ".")
    return _clip(sid, prefix)