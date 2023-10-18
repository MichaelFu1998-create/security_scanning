def pprint(arr, columns=('temperature', 'luminosity'),
           names=('Temperature (Kelvin)', 'Luminosity (solar units)'),
           max_rows=32, precision=2):
    """
    Create a pandas DataFrame from a numpy ndarray.

    By default use temp and lum with max rows of 32 and precision of 2.

    arr - An numpy.ndarray.
    columns - The columns to include in the pandas DataFrame. Defaults to
              temperature and luminosity.
    names - The column names for the pandas DataFrame. Defaults to
            Temperature and Luminosity.
    max_rows - If max_rows is an integer then set the pandas
               display.max_rows option to that value. If max_rows
               is True then set display.max_rows option  to 1000.
    precision - An integer to set the pandas precision option.
    """
    if max_rows is True:
        pd.set_option('display.max_rows', 1000)
    elif type(max_rows) is int:
        pd.set_option('display.max_rows', max_rows)
    pd.set_option('precision', precision)
    df = pd.DataFrame(arr.flatten(), index=arr['id'].flatten(),
                      columns=columns)
    df.columns = names
    return df.style.format({names[0]: '{:.0f}',
                            names[1]: '{:.2f}'})