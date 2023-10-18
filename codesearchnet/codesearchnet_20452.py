def lines2less(lines):
    """
    input: lines = list / iterator of strings
    eg: lines = ["This is the first line", "This is the second line"]

    output: print those lines to stdout if the output is short + narrow
            otherwise print the lines to less
    """
    lines = iter(lines) #cast list to iterator

    #print output to stdout if small, otherwise to less
    has_term = True
    terminal_cols = 100
    try:
        terminal_cols = terminal_size()
    except:
        #getting terminal info failed -- maybe it's a
        #weird situation like running through cron
        has_term = False

    MAX_CAT_ROWS = 20  #if there are <= this many rows then print to screen

    first_rows = list(itertools.islice(lines,0,MAX_CAT_ROWS))
    wide = any(len(l) > terminal_cols for l in first_rows)

    use_less = False
    if has_term and (wide or len(first_rows) == MAX_CAT_ROWS):
        use_less = True

    lines = itertools.chain(first_rows, lines)
    lines = six.moves.map(lambda x: x + '\n', lines)

    if use_less:
        lesspager(lines)
    else:
        for l in lines:
            sys.stdout.write(l)