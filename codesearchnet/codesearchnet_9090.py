def tz_convert(dt, to_tz, from_tz=None) -> str:
    """
    Convert to tz

    Args:
        dt: date time
        to_tz: to tz
        from_tz: from tz - will be ignored if tz from dt is given

    Returns:
        str: date & time

    Examples:
        >>> dt_1 = pd.Timestamp('2018-09-10 16:00', tz='Asia/Hong_Kong')
        >>> tz_convert(dt_1, to_tz='NY')
        '2018-09-10 04:00:00-04:00'
        >>> dt_2 = pd.Timestamp('2018-01-10 16:00')
        >>> tz_convert(dt_2, to_tz='HK', from_tz='NY')
        '2018-01-11 05:00:00+08:00'
        >>> dt_3 = '2018-09-10 15:00'
        >>> tz_convert(dt_3, to_tz='NY', from_tz='JP')
        '2018-09-10 02:00:00-04:00'
    """
    logger = logs.get_logger(tz_convert, level='info')
    f_tz, t_tz = get_tz(from_tz), get_tz(to_tz)

    from_dt = pd.Timestamp(str(dt), tz=f_tz)
    logger.debug(f'converting {str(from_dt)} from {f_tz} to {t_tz} ...')
    return str(pd.Timestamp(str(from_dt), tz=t_tz))