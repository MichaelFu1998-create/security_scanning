def jam_pack(jam, **kwargs):
    '''Pack data into a jams sandbox.

    If not already present, this creates a `muda` field within `jam.sandbox`,
    along with `history`, `state`, and version arrays which are populated by
    deformation objects.

    Any additional fields can be added to the `muda` sandbox by supplying
    keyword arguments.

    Parameters
    ----------
    jam : jams.JAMS
        A JAMS object

    Returns
    -------
    jam : jams.JAMS
        The updated JAMS object

    Examples
    --------
    >>> jam = jams.JAMS()
    >>> muda.jam_pack(jam, my_data=dict(foo=5, bar=None))
    >>> jam.sandbox
    <Sandbox: muda>
    >>> jam.sandbox.muda
    <Sandbox: state, version, my_data, history>
    >>> jam.sandbox.muda.my_data
    {'foo': 5, 'bar': None}
    '''

    if not hasattr(jam.sandbox, 'muda'):
        # If there's no mudabox, create one
        jam.sandbox.muda = jams.Sandbox(history=[],
                                        state=[],
                                        version=dict(muda=version,
                                                     librosa=librosa.__version__,
                                                     jams=jams.__version__,
                                                     pysoundfile=psf.__version__))

    elif not isinstance(jam.sandbox.muda, jams.Sandbox):
        # If there is a muda entry, but it's not a sandbox, coerce it
        jam.sandbox.muda = jams.Sandbox(**jam.sandbox.muda)

    jam.sandbox.muda.update(**kwargs)

    return jam