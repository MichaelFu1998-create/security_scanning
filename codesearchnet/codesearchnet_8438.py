def round_data(filter_data):
    """ round the data"""
    for index, _ in enumerate(filter_data):
        filter_data[index][0] = round(filter_data[index][0] / 100.0) * 100.0
    return filter_data