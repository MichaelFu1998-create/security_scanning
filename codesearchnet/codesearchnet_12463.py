def lib2to3_unparse(node, *, hg=False):
    """Given a lib2to3 node, return its string representation."""
    code = str(node)
    if hg:
        from retype_hgext import apply_job_security
        code = apply_job_security(code)
    return code