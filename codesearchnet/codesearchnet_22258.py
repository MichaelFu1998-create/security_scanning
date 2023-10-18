def add_link(cls, attr, title='', display=''):
        """Adds a ``list_display`` attribute that appears as a link to the
        django admin change page for the type of object being shown. Supports
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
            the row: ``str(obj)`` .  This parameter supports django
            templating, the context for which contains a dictionary key named
            "obj" with the value being the object for the row.

        Example usage:

        .. code-block:: python

            # ---- admin.py file ----

            base = fancy_modeladmin('id')
            base.add_link('author', 'Our Authors',
                '{{obj.name}} (id={{obj.id}})')

            @admin.register(Book)
            class BookAdmin(base):
                pass

        The django admin change page for the Book class would have a column
        for "id" and another titled "Our Authors". The "Our Authors" column
        would have a link for each Author object referenced by "book.author".
        The link would go to the Author django admin change listing. The
        display of the link would be the name of the author with the id in
        brakcets, e.g. "Douglas Adams (id=42)"
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

        def _link(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            text = _obj_display(field_obj, _display)
            return admin_obj_link(field_obj, text)
        _link.short_description = title
        _link.allow_tags = True
        _link.admin_order_field = attr

        setattr(cls, fn_name, _link)