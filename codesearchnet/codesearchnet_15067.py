def load_and_dump(create_loader, create_dumper, load_and_dump_):
    """:return: a function that has the doc string of
      :paramref:`load_and_dump_`
      additional arguments to this function are passed on to
      :paramref:`load_and_dump_`.

    :param create_loader: a loader, e.g.
      :class:`knittingpattern.Loader.PathLoader`
    :param create_dumper: a dumper, e.g.
      :class:`knittingpattern.Dumper.ContentDumper`
    :param load_and_dump_: a function to call with the loaded content.
      The arguments to both, :paramref:`create_dumper` and,
      :paramref:`create_loader`
      will be passed to :paramref:`load_and_dump_`.
      Any additional arguments to the return value are also passed to
      :paramref:`load_and_dump_`.
      The return value of :paramref:`load_and_dump_` is passed back to the
      :paramref:`Dumper`.

    .. seealso:: :func:`decorate_load_and_dump`
    """
    @wraps(load_and_dump_)
    def load_and_dump__(*args1, **kw):
        """Return the loader."""
        def load(*args2):
            """Return the dumper."""
            def dump(*args3):
                """Dump the object."""
                return load_and_dump_(*(args2 + args3 + args1), **kw)
            return create_dumper(dump)
        return create_loader(load)
    return load_and_dump__