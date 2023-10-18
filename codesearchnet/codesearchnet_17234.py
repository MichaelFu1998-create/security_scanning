def has_translocation_increases_activity(data: Dict) -> bool:
    """Check if the translocation of source causes activity of target."""
    return part_has_modifier(data, SUBJECT, TRANSLOCATION) and part_has_modifier(data, OBJECT, ACTIVITY)