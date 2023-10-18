def save_as(self):
        """
        Return True if the buffer was saved
        """
        chooser = ShoebotFileChooserDialog(_('Save File'), None, Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT,
                                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        chooser.set_do_overwrite_confirmation(True)
        chooser.set_transient_for(self)
        saved = chooser.run() == Gtk.ResponseType.ACCEPT
        if saved:
            old_filename = self.filename
            self.source_buffer.filename = chooser.get_filename()
            if not self.save():
                self.filename = old_filename
        chooser.destroy()
        return saved