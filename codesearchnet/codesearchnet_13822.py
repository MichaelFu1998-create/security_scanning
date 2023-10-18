def _create_view(self, name="shoebot-output"):
        """
        Create the gtk.TextView inside a Gtk.ScrolledWindow
        :return: container, text_view
        """
        text_view = Gtk.TextView()
        text_view.set_editable(False)

        fontdesc = Pango.FontDescription("Monospace")
        text_view.modify_font(fontdesc)
        text_view.set_name(name)

        buff = text_view.get_buffer()
        buff.create_tag('error', foreground='red')

        container = Gtk.ScrolledWindow()
        container.add(text_view)
        container.show_all()
        return container, text_view