def is_valid_sound(sound, ts):
    """Check the consistency of a given transcription system conversino"""
    if isinstance(sound, (Marker, UnknownSound)):
        return False
    s1 = ts[sound.name]
    s2 = ts[sound.s]
    return s1.name == s2.name and s1.s == s2.s