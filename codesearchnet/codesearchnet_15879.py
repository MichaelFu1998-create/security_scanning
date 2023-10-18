def get_pointer(self, name, timeout=None):
        """Get a pointer to a named object in the Octave workspace.

        Parameters
        ----------
        name: str
            The name of the object in the Octave workspace.
        timemout: float, optional.
            Time to wait for response from Octave (per line).

        Examples
        --------
        >>> from oct2py import octave
        >>> octave.eval('foo = [1, 2];')
        >>> ptr = octave.get_pointer('foo')
        >>> ptr.value
        array([[ 1.,  2.]])
        >>> ptr.address
        'foo'
        >>> # Can be passed as an argument
        >>> octave.disp(ptr)  # doctest: +SKIP
        1  2

        >>> from oct2py import octave
        >>> sin = octave.get_pointer('sin')  # equivalent to `octave.sin`
        >>> sin.address
        '@sin'
        >>> x = octave.quad(sin, 0, octave.pi())
        >>> x
        2.0

        Notes
        -----
        Pointers can be passed to `feval` or dynamic functions as function arguments.  A pointer passed as a nested value will be passed by value instead.

        Raises
        ------
        Oct2PyError
            If the variable does not exist in the Octave session or is of
            unknown type.

        Returns
        -------
        A variable, object, user class, or function pointer as appropriate.
        """
        exist = self._exist(name)
        isobject = self._isobject(name, exist)

        if exist == 0:
            raise Oct2PyError('"%s" is undefined' % name)

        elif exist == 1:
            return _make_variable_ptr_instance(self, name)

        elif isobject:
            return self._get_user_class(name)

        elif exist in [2, 3, 5]:
            return self._get_function_ptr(name)

        raise Oct2PyError('Unknown type for object "%s"' % name)