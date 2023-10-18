def get_triplet_tuple(a: BaseEntity, b: BaseEntity, c: BaseEntity) -> Tuple[str, str, str, str, str, str]:
    """Get the triple as a tuple of BEL/hashes."""
    return a.as_bel(), a.sha512, b.as_bel(), b.sha512, c.as_bel(), c.sha512