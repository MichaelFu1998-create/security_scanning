def _get_severity(c):
    """
    1. Collect all <severity> and <impact-level> values.
    2. Convert impact-level of 1-3 to MINOR, 4-7 to MODERATE, 8-10 to MAJOR
    3. Map severity -> none to MINOR, natural-disaster to MAJOR, other to UNKNOWN
    4. Pick the highest severity.
    """
    severities = c.feu.xpath('event-indicators/event-indicator/event-severity/text()|event-indicators/event-indicator/severity/text()')
    impacts = c.feu.xpath('event-indicators/event-indicator/event-impact/text()|event-indicators/event-indicator/impact/text()')

    severities = [convert_severity[s] for s in severities]
    impacts = [convert_impact[i] for i in impacts]

    return ['UNKNOWN', 'MINOR', 'MODERATE', 'MAJOR'][max(itertools.chain(severities, impacts))]