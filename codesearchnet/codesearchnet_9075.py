def to_hour(num) -> str:
    """
    Convert YAML input to hours

    Args:
        num: number in YMAL file, e.g., 900, 1700, etc.

    Returns:
        str

    Examples:
        >>> to_hour(900)
        '09:00'
        >>> to_hour(1700)
        '17:00'
    """
    to_str = str(int(num))
    return pd.Timestamp(f'{to_str[:-2]}:{to_str[-2:]}').strftime('%H:%M')