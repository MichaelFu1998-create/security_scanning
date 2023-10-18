def prepare_c3_time_series(data: List[Tuple[int, int]], y_axis_label: str = 'y', x_axis_label: str = 'x') -> str:
    """Prepare C3 JSON string dump for a time series.

    :param data: A list of tuples [(year, count)]
    :param y_axis_label: The Y axis label
    :param x_axis_label: X axis internal label. Should be left as default 'x')
    """
    years, counter = zip(*data)

    years = [
        datetime.date(year, 1, 1).isoformat()
        for year in years
    ]

    return json.dumps([
        [x_axis_label] + list(years),
        [y_axis_label] + list(counter)
    ])