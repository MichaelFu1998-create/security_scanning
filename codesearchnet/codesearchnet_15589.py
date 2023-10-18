def parse(data):
    """
    Parse the given ChangeLog data into a list of Hashes.

    @param [String] data File data from the ChangeLog.md
    @return [Array<Hash>] Parsed data, e.g. [{ 'version' => ..., 'url' => ..., 'date' => ..., 'content' => ...}, ...]
    """

    sections = re.compile("^## .+$", re.MULTILINE).split(data)
    headings = re.findall("^## .+?$", data, re.MULTILINE)
    sections.pop(0)
    parsed = []

    def func(h, s):
        p = parse_heading(h)
        p["content"] = s
        parsed.append(p)

    list(map(func, headings, sections))
    return parsed