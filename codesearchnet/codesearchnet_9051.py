def bdp(tickers, flds, **kwargs):
    """
    Bloomberg reference data

    Args:
        tickers: tickers
        flds: fields to query
        **kwargs: bbg overrides

    Returns:
        pd.DataFrame

    Examples:
        >>> bdp('IQ US Equity', 'Crncy', raw=True)
                 ticker  field value
        0  IQ US Equity  Crncy   USD
        >>> bdp('IQ US Equity', 'Crncy').reset_index()
                 ticker crncy
        0  IQ US Equity   USD
    """
    logger = logs.get_logger(bdp, level=kwargs.pop('log', logs.LOG_LEVEL))
    con, _ = create_connection()
    ovrds = assist.proc_ovrds(**kwargs)

    logger.info(
        f'loading reference data from Bloomberg:\n'
        f'{assist.info_qry(tickers=tickers, flds=flds)}'
    )
    data = con.ref(tickers=tickers, flds=flds, ovrds=ovrds)
    if not kwargs.get('cache', False): return [data]

    qry_data = []
    for r, snap in data.iterrows():
        subset = [r]
        data_file = storage.ref_file(
            ticker=snap.ticker, fld=snap.field, ext='pkl', **kwargs
        )
        if data_file:
            if not files.exists(data_file): qry_data.append(data.iloc[subset])
            files.create_folder(data_file, is_file=True)
            data.iloc[subset].to_pickle(data_file)

    return qry_data