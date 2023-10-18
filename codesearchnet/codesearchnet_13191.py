def pattern_to_mireval(ann):
    '''Convert a pattern_jku annotation object to mir_eval format.

    Parameters
    ----------
    ann : jams.Annotation
        Must have `namespace='pattern_jku'`

    Returns
    -------
    patterns : list of list of tuples
        - `patterns[x]` is a list containing all occurrences of pattern x

        - `patterns[x][y]` is a list containing all notes for
           occurrence y of pattern x

        - `patterns[x][y][z]` contains a time-note tuple
          `(time, midi note)`
    '''

    # It's easier to work with dictionaries, since we can't assume
    # sequential pattern or occurrence identifiers

    patterns = defaultdict(lambda: defaultdict(list))

    # Iterate over the data in interval-value format

    for time, observation in zip(*ann.to_event_values()):

        pattern_id = observation['pattern_id']
        occurrence_id = observation['occurrence_id']
        obs = (time, observation['midi_pitch'])

        # Push this note observation into the correct pattern/occurrence
        patterns[pattern_id][occurrence_id].append(obs)

    # Convert to list-list-tuple format for mir_eval
    return [list(_.values()) for _ in six.itervalues(patterns)]