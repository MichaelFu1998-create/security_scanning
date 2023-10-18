def _parse_iedb_response(response):
    """Take the binding predictions returned by IEDB's web API
    and parse them into a DataFrame

    Expect response to look like:
    allele  seq_num start   end length  peptide ic50   percentile_rank
    HLA-A*01:01 1   2   10  9   LYNTVATLY   2145.70 3.7
    HLA-A*01:01 1   5   13  9   TVATLYCVH   2216.49 3.9
    HLA-A*01:01 1   7   15  9   ATLYCVHQR   2635.42 5.1
    HLA-A*01:01 1   4   12  9   NTVATLYCV   6829.04 20
    HLA-A*01:01 1   1   9   9   SLYNTVATL   8032.38 24
    HLA-A*01:01 1   8   16  9   TLYCVHQRI   8853.90 26
    HLA-A*01:01 1   3   11  9   YNTVATLYC   9865.62 29
    HLA-A*01:01 1   6   14  9   VATLYCVHQ   27575.71    58
    HLA-A*01:01 1   10  18  9   YCVHQRIDV   48929.64    74
    HLA-A*01:01 1   9   17  9   LYCVHQRID   50000.00    75
    """
    if len(response) == 0:
        raise ValueError("Empty response from IEDB!")
    df = pd.read_csv(io.BytesIO(response), delim_whitespace=True, header=0)

    # pylint doesn't realize that df is a DataFrame, so tell is
    assert type(df) == pd.DataFrame
    df = pd.DataFrame(df)

    if len(df) == 0:
        raise ValueError(
            "No binding predictions in response from IEDB: %s" % (response,))
    required_columns = [
        "allele",
        "peptide",
        "ic50",
        "start",
        "end",
    ]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                "Response from IEDB is missing '%s' column: %s. Full "
                "response:\n%s" % (
                    column,
                    df.ix[0],
                    response))
    # since IEDB has allowed multiple column names for percentile rank,
    # we're defensively normalizing all of them to just 'rank'
    df = df.rename(columns={
        "percentile_rank": "rank",
        "percentile rank": "rank"})
    return df