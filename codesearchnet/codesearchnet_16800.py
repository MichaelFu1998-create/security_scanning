def pick_coda_from_letter(letter):
    """Picks only a coda from a Hangul letter.  It returns ``None`` if the
    given letter is not Hangul.
    """
    try:
        __, __, coda = \
            split_phonemes(letter, onset=False, nucleus=False, coda=True)
    except ValueError:
        return None
    else:
        return coda