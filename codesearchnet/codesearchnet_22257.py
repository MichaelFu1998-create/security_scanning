def add_display(cls, attr, title=''):
        """Adds a ``list_display`` property without any extra wrappers,
        similar to :func:`add_displays`, but can also change the title.

        :param attr:
            Name of the attribute to add to the display

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

        if not title:
            title = attr.capitalize()

        def _ref(self, obj):
            # use the django mechanism for field value lookup
            _, _, value = lookup_field(attr, obj, cls)
            return value
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = attr

        setattr(cls, fn_name, _ref)