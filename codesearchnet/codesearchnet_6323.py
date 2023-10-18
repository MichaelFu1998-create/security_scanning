def find_bump(target, tag):
    """Identify the kind of release by comparing to existing ones."""
    tmp = tag.split(".")
    existing = [intify(basename(f)) for f in glob(join(target, "[0-9]*.md"))]
    latest = max(existing)
    if int(tmp[0]) > latest[0]:
        return "major"
    elif int(tmp[1]) > latest[1]:
        return "minor"
    else:
        return "patch"