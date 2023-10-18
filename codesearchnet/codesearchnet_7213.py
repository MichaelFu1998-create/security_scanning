def _show_menu(self):
        """Show the overlay menu."""
        # If the current widget in the TabbedWindowWidget has a menu,
        # overlay it on the TabbedWindowWidget.
        current_widget = self._tabbed_window.get_current_widget()
        if hasattr(current_widget, 'get_menu_widget'):
            menu_widget = current_widget.get_menu_widget(self._hide_menu)
            overlay = urwid.Overlay(menu_widget, self._tabbed_window,
                                    align='center', width=('relative', 80),
                                    valign='middle', height=('relative', 80))
            self._urwid_loop.widget = overlay