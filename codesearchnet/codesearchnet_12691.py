def split_stdout_lines(stdout):
    """
    Given the standard output from NetMHC/NetMHCpan/NetMHCcons tools,
    drop all {comments, lines of hyphens, empty lines} and split the
    remaining lines by whitespace.
    """
    # all the NetMHC formats use lines full of dashes before any actual
    # binding results
    seen_dash = False
    for l in stdout.split("\n"):
        l = l.strip()
        # wait for a line like '----------' before trying to parse entries
        # have to include multiple dashes here since NetMHC 4.0 sometimes
        # gives negative positions in its "peptide" input mode
        if l.startswith("---"):
            seen_dash = True
            continue
        if not seen_dash:
            continue
        # ignore empty lines and comments
        if not l or l.startswith("#"):
            continue
        # beginning of headers in NetMHC
        if any(l.startswith(word) for word in NETMHC_TOKENS):
            continue
        yield l.split()