def piano_roll(annotation, sr=22050, length=None, **kwargs):
    '''Sonify a piano-roll

    This uses mir_eval.sonify.time_frequency, and is appropriate
    for sparse transcription data, e.g., annotations in the `note_midi`
    namespace.
    '''

    intervals, pitches = annotation.to_interval_values()

    # Construct the pitchogram
    pitch_map = {f: idx for idx, f in enumerate(np.unique(pitches))}

    gram = np.zeros((len(pitch_map), len(intervals)))

    for col, f in enumerate(pitches):
        gram[pitch_map[f], col] = 1

    return filter_kwargs(mir_eval.sonify.time_frequency,
                         gram, pitches, intervals,
                         sr, length=length, **kwargs)