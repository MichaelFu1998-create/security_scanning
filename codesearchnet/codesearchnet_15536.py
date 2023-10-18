def blocksearch(block, name):
    """ Recursive search for name in block (inner blocks)
    Args:
        name (str): search term
    Returns:
        Block OR False
    """
    if hasattr(block, 'tokens'):
        for b in block.tokens[1]:
            b = (b if hasattr(b, 'raw') and b.raw() == name else blocksearch(
                b, name))
            if b:
                return b
    return False