def _echo_method(self, method):
        """Given a method, return a method that runs the internal
        method and echos the result.
        """
        @functools.wraps(method)
        def func(*args, **kwargs):
            # Echo warning if this method is deprecated.
            if getattr(method, 'deprecated', False):
                debug.log('This method is deprecated in Tower 3.0.', header='warning')

            result = method(*args, **kwargs)

            # If this was a request that could result in a modification
            # of data, print it in Ansible coloring.
            color_info = {}
            if isinstance(result, dict) and 'changed' in result:
                if result['changed']:
                    color_info['fg'] = 'yellow'
                else:
                    color_info['fg'] = 'green'

            # Piece together the result into the proper format.
            format = getattr(self, '_format_%s' % (getattr(method, 'format_freezer', None) or settings.format))
            output = format(result)

            # Perform the echo.
            secho(output, **color_info)
        return func