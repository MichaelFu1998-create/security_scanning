def get_splice_data():
    """
    Load the mushroom dataset, split it into X and y, and then call the label encoder to get an integer y column.

    :return:
    """

    df = pd.read_csv('source_data/splice/splice.csv')
    X = df.reindex(columns=[x for x in df.columns.values if x != 'class'])
    X['dna'] = X['dna'].map(lambda x: list(str(x).strip()))
    for idx in range(60):
        X['dna_%d' % (idx, )] = X['dna'].map(lambda x: x[idx])
    del X['dna']

    y = df.reindex(columns=['class'])
    y = preprocessing.LabelEncoder().fit_transform(y.values.reshape(-1, ))

    # this data is truly categorical, with no known concept of ordering
    mapping = None

    return X, y, mapping