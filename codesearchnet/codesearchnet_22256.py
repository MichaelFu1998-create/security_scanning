def fancy_modeladmin(*args):
    """Returns a new copy of a :class:`FancyModelAdmin` class (a class, not
    an instance!). This can then be inherited from when declaring a model
    admin class. The :class:`FancyModelAdmin` class has additional methods
    for managing the ``list_display`` attribute.

    :param ``*args``: [optional] any arguments given will be added to the
        ``list_display`` property using regular django ``list_display``
        functionality.

    This function is meant as a replacement for :func:`make_admin_obj_mixin`,
    it does everything the old one does with fewer bookkeeping needs for the
    user as well as adding functionality.

    Example usage:

    .. code-block:: python

        # ---- models.py file ----
        class Author(models.Model):
            name = models.CharField(max_length=100)


        class Book(models.Model):
            title = models.CharField(max_length=100)
            author = models.ForeignKey(Author, on_delete=models.CASCADE)


    .. code-block:: python

        # ---- admin.py file ----
        @admin.register(Author)
        class Author(admin.ModelAdmin):
            list_display = ('name', )


        base = fany_list_display_modeladmin()
        base.add_displays('id', 'name')
        base.add_obj_link('author', 'Our Authors',
            '{{obj.name}} (id={{obj.id}})')

        @admin.register(Book)
        class BookAdmin(base):
            list_display = ('name', 'show_author')


    A sample django admin page for "Book" would have the table:

    +----+---------------------------------+------------------------+
    | ID | Name                            | Our Authors            |
    +====+=================================+========================+
    |  1 | Hitchhikers Guide To The Galaxy | *Douglas Adams (id=1)* |
    +----+---------------------------------+------------------------+
    |  2 | War and Peace                   | *Tolstoy (id=2)*       |
    +----+---------------------------------+------------------------+
    |  3 | Dirk Gently                     | *Douglas Adams (id=1)* |
    +----+---------------------------------+------------------------+


    See :class:`FancyModelAdmin` for a full list of functionality
    provided by the returned base class.
    """
    global klass_count

    klass_count += 1
    name = 'DynamicAdminClass%d' % klass_count

    # clone the admin class
    klass = type(name, (FancyModelAdmin,), {})
    klass.list_display = []
    if len(args) > 0:
        klass.add_displays(*args)

    return klass