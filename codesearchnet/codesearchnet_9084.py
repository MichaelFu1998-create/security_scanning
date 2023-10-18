def shift_time(start_time, mins) -> str:
    """
    Shift start time by mins

    Args:
        start_time: start time in terms of HH:MM string
        mins: number of minutes (+ / -)

    Returns:
        end time in terms of HH:MM string
    """
    s_time = pd.Timestamp(start_time)
    e_time = s_time + np.sign(mins) * pd.Timedelta(f'00:{abs(mins)}:00')
    return e_time.strftime('%H:%M')