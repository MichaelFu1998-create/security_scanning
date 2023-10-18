def create_timeline(year_counter: typing.Counter[int]) -> List[Tuple[int, int]]:
    """Complete the Counter timeline.

    :param Counter year_counter: counter dict for each year
    :return: complete timeline
    """
    if not year_counter:
        return []

    from_year = min(year_counter) - 1
    until_year = datetime.now().year + 1

    return [
        (year, year_counter.get(year, 0))
        for year in range(from_year, until_year)
    ]