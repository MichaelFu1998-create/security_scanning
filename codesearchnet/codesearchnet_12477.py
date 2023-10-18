def fix_line_numbers(body):
    r"""Recomputes all line numbers based on the number of \n characters."""
    maxline = 0
    for node in body.pre_order():
        maxline += node.prefix.count('\n')
        if isinstance(node, Leaf):
            node.lineno = maxline
            maxline += str(node.value).count('\n')