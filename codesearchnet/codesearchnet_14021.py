def _create_view(self, name="shoebot-output"):
        """ Create the gtk.TextView used for shell output """
        view = Gtk.TextView()
        view.set_editable(False)

        fontdesc = Pango.FontDescription("Monospace")
        view.modify_font(fontdesc)
        view.set_name(name)

        buff = view.get_buffer()
        buff.create_tag('error', foreground='red')
        return view