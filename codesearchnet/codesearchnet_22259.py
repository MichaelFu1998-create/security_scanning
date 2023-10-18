def add_object(cls, attr, title='', display=''):
        """Adds a ``list_display`` attribute showing an object.  Supports
        double underscore attribute name dereferencing.

        :param attr:
            Name of the attribute to dereference from the corresponding
            object, i.e. what will be lined to.  This name supports double
            underscore object link referencing for ``models.ForeignKey``
            members.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to the string representation of the object for
            the row: ``str(obj)``.  This parameter supports django templating,
            the context for which contains a dictionary key named "obj" with
            the value being the object for the row.
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

        if not title:
            title = attr.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # referenced the inner function won't see it, so assign it for use
        _display = display

        def _ref(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            return _obj_display(field_obj, _display)
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = attr

        setattr(cls, fn_name, _ref)