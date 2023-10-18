def format_arxiv_id(arxiv_id):
    """Properly format arXiv IDs."""
    if arxiv_id and "/" not in arxiv_id and "arXiv" not in arxiv_id:
        return "arXiv:%s" % (arxiv_id,)
    elif arxiv_id and '.' not in arxiv_id and arxiv_id.lower().startswith('arxiv:'):
        return arxiv_id[6:]  # strip away arxiv: for old identifiers
    else:
        return arxiv_id