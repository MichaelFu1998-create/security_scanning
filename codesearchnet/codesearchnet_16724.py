def to_frame(self, *args):
        """Convert the cells in the view into a DataFrame object.

        If ``args`` is not given, this method returns a DataFrame that
        has an Index or a MultiIndex depending of the number of
        cells parameters and columns each of which corresponds to each
        cells included in the view.

        ``args`` can be given to calculate cells values and limit the
        DataFrame indexes to the given arguments.

        The cells in this view may have different number of parameters,
        but parameters shared among multiple cells
        must appear in the same position in all the parameter lists.
        For example,
        Having ``foo()``, ``bar(x)`` and ``baz(x, y=1)`` is okay
        because the shared parameter ``x`` is always the first parameter,
        but this method does not work if the view has ``quz(x, z=2, y=1)``
        cells in addition to the first three cells, because ``y`` appears
        in different positions.

        Args:
            args(optional): multiple arguments,
               or an iterator of arguments to the cells.
        """
        if sys.version_info < (3, 6, 0):
            from collections import OrderedDict

            impls = OrderedDict()
            for name, obj in self.items():
                impls[name] = obj._impl
        else:
            impls = get_impls(self)

        return _to_frame_inner(impls, args)