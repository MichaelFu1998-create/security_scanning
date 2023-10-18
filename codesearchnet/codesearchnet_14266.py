def update_var(self, name, value):
        """
        :return: success, err_msg_if_failed
        """
        widget = self.widgets.get(name)
        if widget is None:
            return False, 'No widget found matching, {}'.format(name)

        try:
            if isinstance(widget, Gtk.CheckButton):
                widget.set_active(value)
                return True, widget.get_active()
            elif isinstance(widget, Gtk.Entry):
                widget.set_text(value)
                return True, widget.get_text()
            else:
                widget.set_value(value)
                return True, widget.get_value()
        except Exception as e:
            return False, str(e)