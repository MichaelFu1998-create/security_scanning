def read_bgen(filepath, metafile_filepath=None, samples_filepath=None, verbose=True):
    r""" Read a given BGEN file.

    Parameters
    ----------
    filepath : str
        A bgen file path.
    metafile_filepath : str, optional
        If ``None``, it will try to read the ``filepath + ".metadata"`` file. If this is
        not possible, it will create one. It tries to create one at
        ``filepath + ".metadata"``. If that is also no possible, it tries to create one
        at a temporary folder.
    samples_filepath : str, optional
        A sample file in `gen format <https://goo.gl/bCzo7m>`_.
        If ``samples_filepath`` is provided, sample ids are read from this file.
        Otherwise, it reads from the bgen file itself if possible. Defaults to ``None``.
    verbose : bool, optional
        ``True`` to show progress; ``False`` otherwise. Defaults to ``True``.

    Returns
    -------
    variants : :class:`dask.dataFrame.DataFrame`
        Variant position, chromosomes, rsids, etc.
    samples : :class:`pandas.Series`
        Sample identifications.
    genotype : list
        List of genotypes.

    Examples
    --------
    .. doctest::

        >>> from bgen_reader import example_files, read_bgen
        >>>
        >>> with example_files("haplotypes.bgen") as filepath:
        ...     bgen = read_bgen(filepath, verbose=False)
        ...     variants = bgen["variants"]
        ...     samples = bgen["samples"]
        ...
        ...     v = variants.loc[0].compute()
        ...     g = bgen["genotype"][0].compute()
        ...     print(v)
        ...     print(samples)
        ...     print(g["probs"][0])
             id rsid chrom  pos  nalleles allele_ids  vaddr
        0  SNP1  RS1     1    1         2        A,G    102
        0    sample_0
        1    sample_1
        2    sample_2
        3    sample_3
        Name: id, dtype: object
        [1. 0. 1. 0.]
    """

    assert_file_exist(filepath)
    assert_file_readable(filepath)

    metafile_filepath = _get_valid_metafile_filepath(filepath, metafile_filepath)
    if not os.path.exists(metafile_filepath):
        if verbose:
            print(
                f"We will create the metafile `{metafile_filepath}`. This file will "
                "speed up further\nreads and only need to be created once. So, please, "
                "bear with me."
            )
        create_metafile(filepath, metafile_filepath, verbose)

    samples = get_samples(filepath, samples_filepath, verbose)
    variants = map_metadata(filepath, metafile_filepath)
    genotype = map_genotype(filepath, metafile_filepath, verbose)

    return dict(variants=variants, samples=samples, genotype=genotype)