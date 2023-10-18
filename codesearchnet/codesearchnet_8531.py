def prepare_feature(best_processed_path, option='train'):
    """
    Transform processed path into feature matrix and output array

    Input
    =====
    best_processed_path: str, path to processed BEST dataset

    option: str, 'train' or 'test'
    """
    # padding for training and testing set
    n_pad = 21
    n_pad_2 = int((n_pad - 1)/2)
    pad = [{'char': ' ', 'type': 'p', 'target': True}]
    df_pad = pd.DataFrame(pad * n_pad_2)

    df = []
    for article_type in article_types:
        df.append(pd.read_csv(os.path.join(best_processed_path, option, 'df_best_{}_{}.csv'.format(article_type, option))))
    df = pd.concat(df)
    df = pd.concat((df_pad, df, df_pad)) # pad with empty string feature

    df['char'] = df['char'].map(lambda x: CHARS_MAP.get(x, 80))
    df['type'] = df['type'].map(lambda x: CHAR_TYPES_MAP.get(x, 4))
    df_pad = create_n_gram_df(df, n_pad=n_pad)

    char_row = ['char' + str(i + 1) for i in range(n_pad_2)] + \
               ['char-' + str(i + 1) for i in range(n_pad_2)] + ['char']
    type_row = ['type' + str(i + 1) for i in range(n_pad_2)] + \
               ['type-' + str(i + 1) for i in range(n_pad_2)] + ['type']

    x_char = df_pad[char_row].as_matrix()
    x_type = df_pad[type_row].as_matrix()
    y = df_pad['target'].astype(int).as_matrix()

    return x_char, x_type, y