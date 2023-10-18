def generate_steady_rt_pic(process_data, para_meter, scale, steady_time):
    """ generate rate steady"""
    pic_path_steady = para_meter['filename'] + '_steady.png'
    plt.figure(figsize=(4 * scale, 2.5 * scale))
    for key in process_data.keys():
        if len(process_data[key]) < steady_time:
            steady_time = len(process_data[key])
        plt.scatter(process_data[key][-1 * steady_time:, 0],
                    process_data[key][-1 * steady_time:, 1], label=str(key), s=10)
        steady_value = np.mean(process_data[key][-1 * steady_time:, 1])
        steady_value_5 = steady_value * (1 + 0.05)
        steady_value_10 = steady_value * (1 + 0.1)
        steady_value_ng_5 = steady_value * (1 - 0.05)
        steady_value_ng_10 = steady_value * (1 - 0.1)
        plt.plot(process_data[key][-1 * steady_time:, 0], [steady_value] * steady_time, 'b')
        plt.plot(process_data[key][-1 * steady_time:, 0], [steady_value_5] * steady_time, 'g')
        plt.plot(process_data[key][-1 * steady_time:, 0],
                 [steady_value_ng_5] * steady_time, 'g')
        plt.plot(process_data[key][-1 * steady_time:, 0], [steady_value_10] * steady_time, 'r')
        plt.plot(process_data[key][-1 * steady_time:, 0],
                 [steady_value_ng_10] * steady_time, 'r')
    plt.title(para_meter['title'] + '(steady)')
    plt.xlabel(para_meter['x_axis_name'] + '(steady)')
    plt.ylabel(para_meter['y_axis_name'] + '(steady)')
    plt.legend(loc='upper left')
    plt.savefig(pic_path_steady)
    return pic_path_steady