def iterate_forever(func, *args, **kwargs):
    """Iterate over a finite iterator forever

    When the iterator is exhausted will call the function again to generate a
    new iterator and keep iterating.
    """
    output = func(*args, **kwargs)

    while True:
        try:
            playlist_item = next(output)
            playlist_item.prepare_playback()
            yield playlist_item
        except StopIteration:
            output = func(*args, **kwargs)