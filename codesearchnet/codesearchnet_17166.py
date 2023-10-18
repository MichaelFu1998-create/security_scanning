def prepare_c3(data: Union[List[Tuple[str, int]], Mapping[str, int]],
               y_axis_label: str = 'y',
               x_axis_label: str = 'x',
               ) -> str:
    """Prepares C3 JSON for making a bar chart from a Counter

    :param data: A dictionary of {str: int} to display as bar chart
    :param y_axis_label: The Y axis label
    :param x_axis_label: X axis internal label. Should be left as default 'x')
    :return: A JSON dictionary for making a C3 bar chart
    """
    if not isinstance(data, list):
        data = sorted(data.items(), key=itemgetter(1), reverse=True)

    try:
        labels, values = zip(*data)
    except ValueError:
        log.info(f'no values found for {x_axis_label}, {y_axis_label}')
        labels, values = [], []

    return json.dumps([
        [x_axis_label] + list(labels),
        [y_axis_label] + list(values),
    ])