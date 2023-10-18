def has_degradation_increases_activity(data: Dict) -> bool:
    """Check if the degradation of source causes activity of target."""
    return part_has_modifier(data, SUBJECT, DEGRADATION) and part_has_modifier(data, OBJECT, ACTIVITY)