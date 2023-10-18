def downbeat(annotation, sr=22050, length=None, **kwargs):
    '''Sonify beats and downbeats together.
    '''

    beat_click = mkclick(440 * 2, sr=sr)
    downbeat_click = mkclick(440 * 3, sr=sr)

    intervals, values = annotation.to_interval_values()

    beats, downbeats = [], []

    for time, value in zip(intervals[:, 0], values):
        if value['position'] == 1:
            downbeats.append(time)
        else:
            beats.append(time)

    if length is None:
        length = int(sr * np.max(intervals)) + len(beat_click) + 1

    y = filter_kwargs(mir_eval.sonify.clicks,
                      np.asarray(beats),
                      fs=sr, length=length, click=beat_click)

    y += filter_kwargs(mir_eval.sonify.clicks,
                       np.asarray(downbeats),
                       fs=sr, length=length, click=downbeat_click)

    return y