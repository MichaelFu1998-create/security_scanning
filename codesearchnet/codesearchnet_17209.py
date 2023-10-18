def load_differential_gene_expression(path: str,
                                      gene_symbol_column: str = 'Gene.symbol',
                                      logfc_column: str = 'logFC',
                                      aggregator: Optional[Callable[[List[float]], float]] = None,
                                      ) -> Mapping[str, float]:
    """Load and pre-process a differential gene expression data.

    :param path: The path to the CSV
    :param gene_symbol_column: The header of the gene symbol column in the data frame
    :param logfc_column: The header of the log-fold-change column in the data frame
    :param aggregator: A function that aggregates a list of differential gene expression values. Defaults to
                       :func:`numpy.median`. Could also use: :func:`numpy.mean`, :func:`numpy.average`,
                       :func:`numpy.min`, or :func:`numpy.max`
    :return: A dictionary of {gene symbol: log fold change}
    """
    if aggregator is None:
        aggregator = np.median

    # Load the data frame
    df = pd.read_csv(path)

    # Check the columns exist in the data frame
    assert gene_symbol_column in df.columns
    assert logfc_column in df.columns

    # throw away columns that don't have gene symbols - these represent control sequences
    df = df.loc[df[gene_symbol_column].notnull(), [gene_symbol_column, logfc_column]]

    values = defaultdict(list)

    for _, gene_symbol, log_fold_change in df.itertuples():
        values[gene_symbol].append(log_fold_change)

    return {
        gene_symbol: aggregator(log_fold_changes)
        for gene_symbol, log_fold_changes in values.items()
    }