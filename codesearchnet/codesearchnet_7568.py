def split_code_and_text_blocks(source_file):
    """Return list with source file separated into code and text blocks.

    Returns
    -------
    blocks : list of (label, content)
        List where each element is a tuple with the label ('text' or 'code'),
        and content string of block.
    """
    docstring, rest_of_content = get_docstring_and_rest(source_file)

    blocks = [('text', docstring)]

    pattern = re.compile(
        r'(?P<header_line>^#{20,}.*)\s(?P<text_content>(?:^#.*\s)*)',
        flags=re.M)

    pos_so_far = 0
    for match in re.finditer(pattern, rest_of_content):
        match_start_pos, match_end_pos = match.span()
        code_block_content = rest_of_content[pos_so_far:match_start_pos]
        text_content = match.group('text_content')
        sub_pat = re.compile('^#', flags=re.M)
        text_block_content = dedent(re.sub(sub_pat, '', text_content))
        if code_block_content.strip():
            blocks.append(('code', code_block_content))
        if text_block_content.strip():
            blocks.append(('text', text_block_content))
        pos_so_far = match_end_pos

    remaining_content = rest_of_content[pos_so_far:]
    if remaining_content.strip():
        blocks.append(('code', remaining_content))

    return blocks