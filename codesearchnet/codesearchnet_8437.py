def sum_data(filter_data, is_bw):
    """ caculate sum"""
    for index in range(len(filter_data) - 1):
        if filter_data[index][0] > filter_data[index + 1][0]:
            max_index = index + 1
            break
    else:
        max_index = len(filter_data)
    print("max_index: ", max_index + 1)
    num_jobs = int(round(len(filter_data) * 1.0 / max_index))
    print("num_jobs: ", num_jobs)

    dict_time = Counter(filter_data[:, 0])
    list_sum = []
    for time_index in range(1, max_index + 1):

        if dict_time.get(time_index * 1000, 0) != num_jobs:
            print("[WARNING] Time %d, number of data %d != num_jobs %d" % (
                time_index * 1000, dict_time.get(time_index * 1000, 0), num_jobs
            ))
            continue
        filter_mask = (filter_data[:, 0] == time_index * 1000)

        sum_rst = np.sum(filter_data[filter_mask][:, 1])
        if is_bw:
            sum_rst = sum_rst / 1024
        list_sum.append([time_index, sum_rst])
    return np.array(list_sum)