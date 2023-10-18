def check_docstring(cls):
        """
        Asserts that the class has a docstring, returning it if successful.
        """
        docstring = inspect.getdoc(cls)
        if not docstring:
            breadcrumbs = " -> ".join(t.__name__ for t in inspect.getmro(cls)[:-1][::-1])
            msg = "docstring required for plugin '%s' (%s, defined in %s)"
            args = (cls.__name__, breadcrumbs, cls.__module__)
            raise InternalCashewException(msg % args)

        max_line_length = cls._class_settings.get('max-docstring-length')
        if max_line_length:
            for i, line in enumerate(docstring.splitlines()):
                if len(line) > max_line_length:
                    msg = "docstring line %s of %s is %s chars too long" 
                    args = (i, cls.__name__, len(line) - max_line_length)
                    raise Exception(msg % args)

        return docstring