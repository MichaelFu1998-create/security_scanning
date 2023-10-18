def pitch_hz_to_contour(annotation):
    '''Convert a pitch_hz annotation to a contour'''
    annotation.namespace = 'pitch_contour'
    data = annotation.pop_data()

    for obs in data:
        annotation.append(time=obs.time, duration=obs.duration,
                          confidence=obs.confidence,
                          value=dict(index=0,
                                     frequency=np.abs(obs.value),
                                     voiced=obs.value > 0))
    return annotation