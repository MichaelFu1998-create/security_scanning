def are_domains_equal(domain1, domain2):
    """Compare two International Domain Names.

    :Parameters:
        - `domain1`: domains name to compare
        - `domain2`: domains name to compare
    :Types:
        - `domain1`: `unicode`
        - `domain2`: `unicode`

    :return: True `domain1` and `domain2` are equal as domain names."""

    domain1 = domain1.encode("idna")
    domain2 = domain2.encode("idna")
    return domain1.lower() == domain2.lower()