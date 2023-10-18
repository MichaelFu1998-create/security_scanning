def calculate_diagram_ranges(data):
    """
    Given a numpy array calculate what the ranges of the H-R
    diagram should be.
    """
    data = round_arr_teff_luminosity(data)
    temps = data['temp']
    x_range = [1.05 * np.amax(temps), .95 * np.amin(temps)]
    lums = data['lum']
    y_range = [.50 * np.amin(lums), 2 * np.amax(lums)]
    return (x_range, y_range)