def _clean_animation(desc, parent):
    """
    Cleans up all sorts of special cases that humans want when entering
    an animation from a yaml file.

    1. Loading it from a file
    2. Using just a typename instead of a dict
    3. A single dict representing an animation, with a run: section.
    4. (Legacy) Having a dict with parallel elements run: and animation:
    5. (Legacy) A tuple or list: (animation, run )

    """
    desc = load.load_if_filename(desc) or desc

    if isinstance(desc, str):
        animation = {'typename': desc}

    elif not isinstance(desc, dict):
        raise TypeError('Unexpected type %s in collection' % type(desc))

    elif 'typename' in desc or 'animation' not in desc:
        animation = desc

    else:
        animation = desc.pop('animation', {})
        if isinstance(animation, str):
            animation = {'typename': animation}

        animation['run'] = desc.pop('run', {})
        if desc:
            raise ValueError('Extra animation fields: ' + ', '.join(desc))

    animation.setdefault('typename', DEFAULT_ANIMATION)
    animation = construct.to_type_constructor(animation, ANIMATION_PATH)
    datatype = animation.setdefault('datatype', failed.Failed)
    animation.setdefault('name', datatype.__name__)

    # Children without fps or sleep_time get it from their parents.
    # TODO: We shouldn't have to rewrite our descriptions here!  The
    # animation engine should be smart enough to figure out the right
    # speed to run a subanimation without a run: section.
    run = animation.setdefault('run', {})
    run_parent = parent.setdefault('run', {})
    if not ('fps' in run or 'sleep_time' in run):
        if 'fps' in run_parent:
            run.update(fps=run_parent['fps'])
        elif 'sleep_time' in run_parent:
            run.update(sleep_time=run_parent['sleep_time'])

    return animation