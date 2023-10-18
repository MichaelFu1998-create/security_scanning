def compute_dosage(expec, alt=None):
    r""" Compute dosage from allele expectation.

    Parameters
    ----------
    expec : array_like
        Allele expectations encoded as a samples-by-alleles matrix.
    alt : array_like, optional
        Alternative allele index. If ``None``, the allele having the minor
        allele frequency for the provided ``expec`` is used as the alternative.
        Defaults to ``None``.

    Returns
    -------
    :class:`numpy.ndarray`
        Dosage encoded as an array of size equal to the number of samples.

    Examples
    --------
    .. code-block:: python
        :caption: First a quick-start example.

        >>> from bgen_reader import allele_expectation, compute_dosage
        >>> from bgen_reader import example_files, read_bgen
        >>>
        >>> # Download an example.
        >>> example = example_files("example.32bits.bgen")
        >>> filepath = example.filepath
        >>>
        >>> # Read the example.
        >>> bgen = read_bgen(filepath, verbose=False)
        >>>
        >>> # Extract the allele expectations of the fourth variant.
        >>> variant_idx = 3
        >>> e = allele_expectation(bgen, variant_idx)
        >>>
        >>> # Compute the dosage when considering the first allele
        >>> # as the reference/alternative one.
        >>> alt_allele_idx = 1
        >>> d = compute_dosage(e, alt=alt_allele_idx)
        >>>
        >>> # Print the dosage of the first five samples only.
        >>> print(d[:5])
        [1.96185308 0.00982666 0.01745552 1.00347899 1.01153563]
        >>>
        >>> # Clean-up the example
        >>> example.close()

    .. code-block:: python
        :caption: Genotype probabilities, allele expectations and frequencies.

        >>> from bgen_reader import (
        ...     allele_expectation,
        ...     allele_frequency,
        ...     compute_dosage,
        ...     example_files,
        ...     read_bgen,
        ... )
        >>> from pandas import DataFrame
        >>> from xarray import DataArray
        >>>
        >>> # Download an example
        >>> example = example_files("example.32bits.bgen")
        >>> filepath = example.filepath
        >>>
        >>> # Open the bgen file.
        >>> bgen = read_bgen(filepath, verbose=False)
        >>> variants = bgen["variants"]
        >>> genotype = bgen["genotype"]
        >>> samples = bgen["samples"]
        >>>
        >>> variant_idx = 3
        >>> variant = variants.loc[variant_idx].compute()
        >>> # Print the metadata of the fourth variant.
        >>> print(variant)
                id    rsid chrom   pos  nalleles allele_ids  vaddr
        3  SNPID_5  RSID_5    01  5000         2        A,G  16034

        >>> geno = bgen["genotype"][variant_idx].compute()
        >>> metageno = DataFrame({k: geno[k] for k in ["ploidy", "missing"]},
        ...                      index=samples)
        >>> metageno.index.name = "sample"
        >>> print(metageno) # doctest: +IGNORE_EXCEPTION_DETAIL, +NORMALIZE_WHITESPACE
                    ploidy  missing
        sample
        sample_001       2    False
        sample_002       2    False
        sample_003       2    False
        sample_004       2    False
        ...            ...      ...
        sample_497       2    False
        sample_498       2    False
        sample_499       2    False
        sample_500       2    False
        <BLANKLINE>
        [500 rows x 2 columns]
        >>> p = DataArray(
        ...     geno["probs"],
        ...     name="probability",
        ...     coords={"sample": samples},
        ...     dims=["sample", "genotype"],
        ... )
        >>> # Print the genotype probabilities.
        >>> print(p.to_series().unstack(level=-1)) # doctest: +IGNORE_EXCEPTION_DETAIL, +NORMALIZE_WHITESPACE
        genotype          0        1        2
        sample
        sample_001  0.00488  0.02838  0.96674
        sample_002  0.99045  0.00928  0.00027
        sample_003  0.98932  0.00391  0.00677
        sample_004  0.00662  0.98328  0.01010
        ...             ...      ...      ...
        sample_497  0.00137  0.01312  0.98550
        sample_498  0.00552  0.99423  0.00024
        sample_499  0.01266  0.01154  0.97580
        sample_500  0.00021  0.98431  0.01547
        <BLANKLINE>
        [500 rows x 3 columns]
        >>> alleles = variant["allele_ids"].item().split(",")
        >>> e = DataArray(
        ...     allele_expectation(bgen, variant_idx),
        ...     name="expectation",
        ...     coords={"sample": samples, "allele": alleles},
        ...     dims=["sample", "allele"],
        ... )
        >>> # Print the allele expectations.
        >>> print(e.to_series().unstack(level=-1)) # doctest: +IGNORE_EXCEPTION_DETAIL, +NORMALIZE_WHITESPACE
        allele            A        G
        sample
        sample_001  0.03815  1.96185
        sample_002  1.99017  0.00983
        sample_003  1.98254  0.01746
        sample_004  0.99652  1.00348
        ...             ...      ...
        sample_497  0.01587  1.98413
        sample_498  1.00528  0.99472
        sample_499  0.03687  1.96313
        sample_500  0.98474  1.01526
        <BLANKLINE>
        [500 rows x 2 columns]
        >>> rsid = variant["rsid"].item()
        >>> chrom = variant["chrom"].item()
        >>> variant_name = f"{chrom}:{rsid}"
        >>> f = DataFrame(allele_frequency(e), columns=[variant_name], index=alleles)
        >>> f.index.name = "allele"
        >>> # Allele frequencies.
        >>> print(f) # doctest: +IGNORE_EXCEPTION_DETAIL, +NORMALIZE_WHITESPACE
                01:RSID_5
        allele
        A       305.97218
        G       194.02782
        >>> alt = f.idxmin().item()
        >>> alt_idx = alleles.index(alt)
        >>> d = compute_dosage(e, alt=alt_idx).to_series()
        >>> d = DataFrame(d.values, columns=[f"alt={alt}"], index=d.index)
        >>> # Dosages when considering G as the alternative allele.
        >>> print(d) # doctest: +IGNORE_EXCEPTION_DETAIL, +NORMALIZE_WHITESPACE
                      alt=G
        sample
        sample_001  1.96185
        sample_002  0.00983
        sample_003  0.01746
        sample_004  1.00348
        ...             ...
        sample_497  1.98413
        sample_498  0.99472
        sample_499  1.96313
        sample_500  1.01526
        <BLANKLINE>
        [500 rows x 1 columns]
        >>>
        >>> # Clean-up the example
        >>> example.close()
    """
    if alt is None:
        return expec[..., -1]
    try:
        return expec[:, alt]
    except NotImplementedError:
        alt = asarray(alt, int)
        return asarray(expec, float)[:, alt]