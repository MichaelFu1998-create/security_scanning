def parse_heading(heading):
    """
    Parse a single heading and return a Hash
    The following heading structures are currently valid:
    - ## [v1.0.2](https://github.com/zanui/chef-thumbor/tree/v1.0.1) (2015-03-24)
    - ## [v1.0.2](https://github.com/zanui/chef-thumbor/tree/v1.0.1)
    - ## v1.0.2 (2015-03-24)
    - ## v1.0.2

    @param [String] heading Heading from the ChangeLog File
    @return [Hash] Returns a structured Hash with version, url and date
    """

    heading_structures = [
        r"^## \[(?P<version>.+?)\]\((?P<url>.+?)\)( \((?P<date>.+?)\))?$",
        r"^## (?P<version>.+?)( \((?P<date>.+?)\))?$",
        ]
    captures = {"version": None, "url": None, "date": None}

    for regexp in heading_structures:
        matches = re.match(regexp, heading)
        if matches:
            captures.update(matches.groupdict())
            break
    return captures