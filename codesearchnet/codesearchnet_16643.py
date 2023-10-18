def get_repr(self, obj, referent=None):
        """Return an HTML tree block describing the given object."""
        objtype = type(obj)
        typename = str(objtype.__module__) + "." + objtype.__name__
        prettytype = typename.replace("__builtin__.", "")

        name = getattr(obj, "__name__", "")
        if name:
            prettytype = "%s %r" % (prettytype, name)

        key = ""
        if referent:
            key = self.get_refkey(obj, referent)
        url = reverse('dowser_trace_object', args=(
            typename,
            id(obj)
        ))
        return ('<a class="objectid" href="%s">%s</a> '
                '<span class="typename">%s</span>%s<br />'
                '<span class="repr">%s</span>'
                % (url, id(obj), prettytype, key, get_repr(obj, 100))
                )