def get_conv_widget(self, conv_id):
        """Return an existing or new ConversationWidget."""
        if conv_id not in self._conv_widgets:
            set_title_cb = (lambda widget, title:
                            self._tabbed_window.set_tab(widget, title=title))
            widget = ConversationWidget(
                self._client, self._coroutine_queue,
                self._conv_list.get(conv_id), set_title_cb, self._keys,
                self._datetimefmt
            )
            self._conv_widgets[conv_id] = widget
        return self._conv_widgets[conv_id]