def scaper_to_tag(annotation):
    '''Convert scaper annotations to tag_open'''

    annotation.namespace = 'tag_open'

    data = annotation.pop_data()
    for obs in data:
        annotation.append(time=obs.time, duration=obs.duration,
                          confidence=obs.confidence, value=obs.value['label'])

    return annotation