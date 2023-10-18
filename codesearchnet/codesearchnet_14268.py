def var_added(self, v):
        """
        var was added in the bot while it ran, possibly
        by livecoding

        :param v:
        :return:
        """
        self.add_variable(v)

        self.window.set_size_request(400, 35 * len(self.widgets.keys()))
        self.window.show_all()