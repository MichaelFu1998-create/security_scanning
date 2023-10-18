def parse_gpr(str_expr):
    """parse gpr into AST

    Parameters
    ----------
    str_expr : string
        string with the gene reaction rule to parse

    Returns
    -------
    tuple
        elements ast_tree and gene_ids as a set
    """
    str_expr = str_expr.strip()
    if len(str_expr) == 0:
        return None, set()
    for char, escaped in replacements:
        if char in str_expr:
            str_expr = str_expr.replace(char, escaped)
    escaped_str = keyword_re.sub("__cobra_escape__", str_expr)
    escaped_str = number_start_re.sub("__cobra_escape__", escaped_str)
    tree = ast_parse(escaped_str, "<string>", "eval")
    cleaner = GPRCleaner()
    cleaner.visit(tree)
    eval_gpr(tree, set())  # ensure the rule can be evaluated
    return tree, cleaner.gene_set