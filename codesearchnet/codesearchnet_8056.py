def transpose(label, n_semitones):
    '''Transpose a chord label by some number of semitones

    Parameters
    ----------
    label : str
        A chord string

    n_semitones : float
        The number of semitones to move `label`

    Returns
    -------
    label_transpose : str
        The transposed chord label

    '''

    # Otherwise, split off the note from the modifier
    match = re.match(six.text_type('(?P<note>[A-G][b#]*)(?P<mod>.*)'),
                     six.text_type(label))

    if not match:
        return label

    note = match.group('note')

    new_note = librosa.midi_to_note(librosa.note_to_midi(note) + n_semitones,
                                    octave=False)

    return new_note + match.group('mod')