def var_deleted(self, v):
        """
        var was added in the bot

        :param v:
        :return:
        """
        widget = self.widgets[v.name]

        # widgets are all in a single container ..
        parent = widget.get_parent()
        self.container.remove(parent)
        del self.widgets[v.name]

        self.window.set_size_request(400, 35 * len(self.widgets.keys()))
        self.window.show_all()