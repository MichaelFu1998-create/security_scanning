def translate_column(df, column, translations):
    """
    :param df: (pandas.Dataframe) the dataframe to be translated
    :param column: (str) the column to be translated
    :param translations: (dict) a dictionary of the strings to be categorized and translated
    """
    df[column] = df[column].astype('category')
    translations = [translations[cat]
                    for cat in df[column].cat.categories]
    df[column].cat.rename_categories(translations, inplace=True)