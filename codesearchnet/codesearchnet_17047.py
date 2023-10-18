def preprocessing_excel(path):
    """Preprocess the excel sheet

    :param filepath: filepath of the excel data
    :return: df: pandas dataframe with excel data
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(path):
        raise ValueError("Error: %s file not found" % path)

    # Import Models from Excel sheet, independent for AD and PD
    df = pd.read_excel(path, sheetname=0, header=0)

    # Indexes and column name
    # [log.info(str(x)+': '+str((df.columns.values[x]))) for x in range (0,len(df.columns.values))]

    # Starting from 4: Pathway Name

    # Fill Pathway cells that are merged and are 'NaN' after deleting rows where there is no genes
    df.iloc[:, 0] = pd.Series(df.iloc[:, 0]).fillna(method='ffill')

    # Number of gaps
    # log.info(df.ix[:,6].isnull().sum())

    df = df[df.ix[:, 1].notnull()]
    df = df.reset_index(drop=True)

    # Fill NaN to ceros in PubmedID column
    df.ix[:, 2].fillna(0, inplace=True)

    # Number of gaps in the gene column should be already zero
    if (df.ix[:, 1].isnull().sum()) != 0:
        raise ValueError("Error: Empty cells in the gene column")

    # Check current state
    # df.to_csv('out.csv')

    return df