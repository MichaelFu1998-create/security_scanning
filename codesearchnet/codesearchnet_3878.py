def _register_numpy_extensions(self):
        """
        CommandLine:
            python -m ubelt.util_format FormatterExtensions._register_numpy_extensions

        Example:
            >>> import sys
            >>> import pytest
            >>> import ubelt as ub
            >>> if not ub.modname_to_modpath('numpy'):
            ...     raise pytest.skip()
            >>> # xdoctest: +IGNORE_WHITESPACE
            >>> import numpy as np
            >>> data = np.array([[.2, 42, 5], [21.2, 3, .4]])
            >>> print(ub.repr2(data))
            np.array([[ 0.2, 42. ,  5. ],
                      [21.2,  3. ,  0.4]], dtype=np.float64)
            >>> print(ub.repr2(data, with_dtype=False))
            np.array([[ 0.2, 42. ,  5. ],
                      [21.2,  3. ,  0.4]])
            >>> print(ub.repr2(data, strvals=True))
            [[ 0.2, 42. ,  5. ],
             [21.2,  3. ,  0.4]]
            >>> data = np.empty((0, 10), dtype=np.float64)
            >>> print(ub.repr2(data, strvals=False))
            np.empty((0, 10), dtype=np.float64)
            >>> print(ub.repr2(data, strvals=True))
            []
            >>> data = np.ma.empty((0, 10), dtype=np.float64)
            >>> print(ub.repr2(data, strvals=False))
            np.ma.empty((0, 10), dtype=np.float64)
        """
        import numpy as np
        @self.register(np.ndarray)
        def format_ndarray(data, **kwargs):
            import re
            strvals = kwargs.get('sv', kwargs.get('strvals', False))
            itemsep = kwargs.get('itemsep', ' ')
            precision = kwargs.get('precision', None)
            suppress_small = kwargs.get('supress_small', None)
            max_line_width = kwargs.get('max_line_width', None)
            with_dtype = kwargs.get('with_dtype', kwargs.get('dtype', not strvals))
            newlines = kwargs.pop('nl', kwargs.pop('newlines', 1))

            # if with_dtype and strvals:
            #     raise ValueError('cannot format with strvals and dtype')

            separator = ',' + itemsep

            if strvals:
                prefix = ''
                suffix = ''
            else:
                modname = type(data).__module__
                # substitute shorthand for numpy module names
                np_nice = 'np'
                modname = re.sub('\\bnumpy\\b', np_nice, modname)
                modname = re.sub('\\bma.core\\b', 'ma', modname)

                class_name = type(data).__name__
                if class_name == 'ndarray':
                    class_name = 'array'

                prefix = modname + '.' + class_name + '('

                if with_dtype:
                    dtype_repr = data.dtype.name
                    # dtype_repr = np.core.arrayprint.dtype_short_repr(data.dtype)
                    suffix = ',{}dtype={}.{})'.format(itemsep, np_nice, dtype_repr)
                else:
                    suffix = ')'

            if not strvals and data.size == 0 and data.shape != (0,):
                # Special case for displaying empty data
                prefix = modname + '.empty('
                body = repr(tuple(map(int, data.shape)))
            else:
                body = np.array2string(data, precision=precision,
                                       separator=separator,
                                       suppress_small=suppress_small,
                                       prefix=prefix,
                                       max_line_width=max_line_width)
            if not newlines:
                # remove newlines if we need to
                body = re.sub('\n *', '', body)
            formatted = prefix + body + suffix
            return formatted

        # Hack, make sure we also register numpy floats
        self.register(np.float32)(self.func_registry[float])