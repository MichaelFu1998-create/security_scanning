def piano_roll(annotation, **kwargs):
    '''Plotting wrapper for piano rolls'''
    times, midi = annotation.to_interval_values()

    return mir_eval.display.piano_roll(times, midi=midi, **kwargs)