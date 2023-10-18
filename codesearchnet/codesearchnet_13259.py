def chord(annotation, sr=22050, length=None, **kwargs):
    '''Sonify chords

    This uses mir_eval.sonify.chords.
    '''

    intervals, chords = annotation.to_interval_values()

    return filter_kwargs(mir_eval.sonify.chords,
                         chords, intervals,
                         fs=sr, length=length,
                         **kwargs)