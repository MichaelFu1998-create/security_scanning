def allele_frequency(expec):
    r""" Compute allele frequency from its expectation.

    Parameters
    ----------
    expec : array_like
        Allele expectations encoded as a samples-by-alleles matrix.

    Returns
    -------
    :class:`numpy.ndarray`
        Allele frequencies encoded as a variants-by-alleles matrix.

    Examples
    --------
    .. doctest::

        >>> from bgen_reader import read_bgen, example_files
        >>> from bgen_reader import allele_expectation, allele_frequency
        >>>
        >>> # Download an example
        >>> example = example_files("example.32bits.bgen")
        >>> filepath = example.filepath
        >>>
        >>> bgen = read_bgen(filepath, verbose=False)
        >>>
        >>> variants = bgen["variants"]
        >>> samples = bgen["samples"]
        >>> genotype = bgen["genotype"]
        >>>
        >>> variant = variants[variants["rsid"] == "RSID_6"].compute()
        >>> variant_idx = variant.index.item()
        >>>
        >>> p = genotype[variant_idx].compute()["probs"]
        >>> # For unphased genotypes only.
        >>> e = allele_expectation(bgen, variant_idx)
        >>> f = allele_frequency(e)
        >>>
        >>> alleles = variant["allele_ids"].item().split(",")
        >>> print(alleles[0] + ": {}".format(f[0]))
        A: 229.23103218810434
        >>> print(alleles[1] + ": {}".format(f[1]))
        G: 270.7689678118956
        >>> print(variant)
                id    rsid chrom   pos  nalleles allele_ids  vaddr
        4  SNPID_6  RSID_6    01  6000         2        A,G  19377
        >>>
        >>> # Clean-up the example
        >>> example.close()
    """
    expec = asarray(expec, float)
    if expec.ndim != 2:
        raise ValueError("Expectation matrix must be bi-dimensional.")
    ploidy = expec.shape[-1]
    return expec.sum(-2) / ploidy