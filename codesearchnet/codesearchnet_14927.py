def allele_expectation(bgen, variant_idx):
    r""" Allele expectation.

    Compute the expectation of each allele from the genotype probabilities.

    Parameters
    ----------
    bgen : bgen_file
        Bgen file handler.
    variant_idx : int
        Variant index.

    Returns
    -------
    :class:`numpy.ndarray`
        Samples-by-alleles matrix of allele expectations.

    Note
    ----
    This function supports unphased genotypes only.

    Examples
    --------
    .. doctest::

        >>> from bgen_reader import allele_expectation, example_files, read_bgen
        >>>
        >>> from texttable import Texttable
        >>>
        >>> # Download an example.
        >>> example = example_files("example.32bits.bgen")
        >>> filepath = example.filepath
        >>>
        >>> # Read the example.
        >>> bgen = read_bgen(filepath, verbose=False)
        >>>
        >>> variants = bgen["variants"]
        >>> samples = bgen["samples"]
        >>> genotype = bgen["genotype"]
        >>>
        >>> genotype = bgen["genotype"]
        >>> # This `compute` call will return a pandas data frame,
        >>> variant = variants[variants["rsid"] == "RSID_6"].compute()
        >>> # from which we retrieve the variant index.
        >>> variant_idx = variant.index.item()
        >>> print(variant)
                id    rsid chrom   pos  nalleles allele_ids  vaddr
        4  SNPID_6  RSID_6    01  6000         2        A,G  19377
        >>> genotype = bgen["genotype"]
        >>> # Samples is a pandas series, and we retrieve the
        >>> # sample index from the sample name.
        >>> sample_idx = samples[samples == "sample_005"].index.item()
        >>>
        >>> genotype = bgen["genotype"]
        >>> # This `compute` call will return a dictionary from which
        >>> # we can get the probability matrix the corresponding
        >>> # variant.
        >>> p = genotype[variant_idx].compute()["probs"][sample_idx]
        >>>
        >>> genotype = bgen["genotype"]
        >>> # Allele expectation makes sense for unphased genotypes only,
        >>> # which is the case here.
        >>> e = allele_expectation(bgen, variant_idx)[sample_idx]
        >>>
        >>> genotype = bgen["genotype"]
        >>> alleles = variant["allele_ids"].item().split(",")
        >>>
        >>> genotype = bgen["genotype"]
        >>>
        >>> # Print what we have got in a nice format.
        >>> table = Texttable()
        >>> table = table.add_rows(
        ...     [
        ...         ["", "AA", "AG", "GG", "E[.]"],
        ...         ["p"] + list(p) + ["na"],
        ...         ["#" + alleles[0], 2, 1, 0, e[0]],
        ...         ["#" + alleles[1], 0, 1, 2, e[1]],
        ...     ]
        ... )
        >>> print(table.draw())
        +----+-------+-------+-------+-------+
        |    |  AA   |  AG   |  GG   | E[.]  |
        +====+=======+=======+=======+=======+
        | p  | 0.012 | 0.987 | 0.001 | na    |
        +----+-------+-------+-------+-------+
        | #A | 2     | 1     | 0     | 1.011 |
        +----+-------+-------+-------+-------+
        | #G | 0     | 1     | 2     | 0.989 |
        +----+-------+-------+-------+-------+
        >>>
        >>> # Clean-up.
        >>> example.close()
    """
    geno = bgen["genotype"][variant_idx].compute()
    if geno["phased"]:
        raise ValueError("Allele expectation is define for unphased genotypes only.")

    nalleles = bgen["variants"].loc[variant_idx, "nalleles"].compute().item()
    genotypes = get_genotypes(geno["ploidy"], nalleles)
    expec = []
    for i in range(len(genotypes)):
        count = asarray(genotypes_to_allele_counts(genotypes[i]), float)
        n = count.shape[0]
        expec.append((count.T * geno["probs"][i, :n]).sum(1))

    return stack(expec, axis=0)