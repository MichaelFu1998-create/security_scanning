def get_pair_tuple(a: BaseEntity, b: BaseEntity) -> Tuple[str, str, str, str]:
    """Get the pair as a tuple of BEL/hashes."""
    return a.as_bel(), a.sha512, b.as_bel(), b.sha512