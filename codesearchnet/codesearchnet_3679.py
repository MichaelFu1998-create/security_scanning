def get_cars_data():
    """
    Load the cars dataset, split it into X and y, and then call the label encoder to get an integer y column.

    :return:
    """

    df = pd.read_csv('source_data/cars/car.data.txt')
    X = df.reindex(columns=[x for x in df.columns.values if x != 'class'])
    y = df.reindex(columns=['class'])
    y = preprocessing.LabelEncoder().fit_transform(y.values.reshape(-1, ))

    mapping = [
        {'col': 'buying', 'mapping': [('vhigh', 0), ('high', 1), ('med', 2), ('low', 3)]},
        {'col': 'maint', 'mapping': [('vhigh', 0), ('high', 1), ('med', 2), ('low', 3)]},
        {'col': 'doors', 'mapping': [('2', 0), ('3', 1), ('4', 2), ('5more', 3)]},
        {'col': 'persons', 'mapping': [('2', 0), ('4', 1), ('more', 2)]},
        {'col': 'lug_boot', 'mapping': [('small', 0), ('med', 1), ('big', 2)]},
        {'col': 'safety', 'mapping': [('high', 0), ('med', 1), ('low', 2)]},
    ]

    return X, y, mapping