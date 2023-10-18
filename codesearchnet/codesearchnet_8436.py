def process_rt_data(source_data, is_bw=False):
    """ process data"""
    print("source_data length:", len(source_data))
    filter_data = {}
    for index in range(2):

        filter_mask = source_data[:, 2] == index

        if np.any(filter_mask):
            filter_data[index] = sum_data(round_data(source_data[filter_mask]), is_bw)
    return filter_data