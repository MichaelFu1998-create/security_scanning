def to_download():
    """
        Build interval of urls to download.
        We always get the first file of the next day.
        Ex: 2013-01-01 => 2013-01-02.0000
    """
    first_day = parse(interval_first)
    last_day = parse(interval_last)
    format_change = parse('2010-06-14')
    one_day = datetime.timedelta(1)
    cur_day = first_day
    url_list = []
    while cur_day < last_day:
        fname = filename.format(day=cur_day.strftime("%Y%m%d"))
        if cur_day > format_change:
            cur_day += one_day
            url = base_url.format(year_month=cur_day.strftime("%Y.%m"),
                                  file_day=cur_day.strftime("%Y%m%d"))
        else:
            url = base_url_old.format(year_month=cur_day.strftime("%Y.%m"),
                                      file_day=cur_day.strftime("%Y%m%d"))
            cur_day += one_day
        url_list.append((fname, url))
    return sorted(url_list, key=lambda tup: tup[0], reverse=True)