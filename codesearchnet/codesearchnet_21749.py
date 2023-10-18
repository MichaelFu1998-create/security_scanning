def get_dataframe_from_variable(nc, data_var):
    """ Returns a Pandas DataFrame of the data.
        This always returns positive down depths
    """
    time_var = nc.get_variables_by_attributes(standard_name='time')[0]

    depth_vars = nc.get_variables_by_attributes(axis=lambda v: v is not None and v.lower() == 'z')
    depth_vars += nc.get_variables_by_attributes(standard_name=lambda v: v in ['height', 'depth' 'surface_altitude'], positive=lambda x: x is not None)

    # Find the correct depth variable
    depth_var = None
    for d in depth_vars:
        try:
            if d._name in data_var.coordinates.split(" ") or d._name in data_var.dimensions:
                depth_var = d
                break
        except AttributeError:
            continue

    times  = netCDF4.num2date(time_var[:], units=time_var.units, calendar=getattr(time_var, 'calendar', 'standard'))
    original_times_size = times.size

    if depth_var is None and hasattr(data_var, 'sensor_depth'):
        depth_type = get_type(data_var.sensor_depth)
        depths = np.asarray([data_var.sensor_depth] * len(times)).flatten()
        values = data_var[:].flatten()
    elif depth_var is None:
        depths = np.asarray([np.nan] * len(times)).flatten()
        depth_type = get_type(depths)
        values = data_var[:].flatten()
    else:
        depths = depth_var[:]
        depth_type = get_type(depths)
        if len(data_var.shape) > 1:
            times = np.repeat(times, depths.size)
            depths = np.tile(depths, original_times_size)
            values = data_var[:, :].flatten()
        else:
            values = data_var[:].flatten()

        if getattr(depth_var, 'positive', 'down').lower() == 'up':
            logger.warning("Converting depths to positive down before returning the DataFrame")
            depths = depths * -1

    # https://github.com/numpy/numpy/issues/4595
    # We can't call astype on a MaskedConstant
    if (
        isinstance(depths, np.ma.core.MaskedConstant) or
        (hasattr(depths, 'mask') and depths.mask.all())
    ):
        depths = np.asarray([np.nan] * len(times)).flatten()

    df = pd.DataFrame({ 'time':   times,
                        'value':  values.astype(data_var.dtype),
                        'unit':   data_var.units if hasattr(data_var, 'units') else np.nan,
                        'depth':  depths.astype(depth_type) })

    df.set_index([pd.DatetimeIndex(df['time']), pd.Float64Index(df['depth'])], inplace=True)
    return df