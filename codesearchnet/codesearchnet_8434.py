def generate_rt_pic(process_data, para_meter, scale):
    """ generate rater pic"""
    pic_path = para_meter['filename'] + '.png'
    plt.figure(figsize=(5.6 * scale, 3.2 * scale))
    for key in process_data.keys():
        plt.plot(process_data[key][:, 0], process_data[key][:, 1], label=str(key))
    plt.title(para_meter['title'])
    plt.xlabel(para_meter['x_axis_name'])
    plt.ylabel(para_meter['y_axis_name'])
    plt.legend(loc='upper left')
    plt.savefig(pic_path)
    return pic_path