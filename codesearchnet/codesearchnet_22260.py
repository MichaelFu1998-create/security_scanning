def add_formatted_field(cls, field, format_string, title=''):
        """Adds a ``list_display`` attribute showing a field in the object
        using a python %formatted string.

        :param field:
            Name of the field in the object.

        :param format_string:
            A old-style (to remain python 2.x compatible) % string formatter
            with a single variable reference. The named ``field`` attribute
            will be passed to the formatter using the "%" operator. 

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``field``
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

        if not title:
            title = field.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # referenced the inner function won't see it, so assign it for use
        _format_string = format_string

        def _ref(self, obj):
            return _format_string % getattr(obj, field)
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = field

        setattr(cls, fn_name, _ref)