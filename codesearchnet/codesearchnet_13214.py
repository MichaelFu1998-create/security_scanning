def note_hz_to_midi(annotation):
    '''Convert a pitch_hz annotation to pitch_midi'''

    annotation.namespace = 'note_midi'

    data = annotation.pop_data()

    for obs in data:
        annotation.append(time=obs.time, duration=obs.duration,
                          confidence=obs.confidence,
                          value=12 * (np.log2(obs.value) - np.log2(440.0)) + 69)

    return annotation