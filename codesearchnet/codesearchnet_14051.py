def main_iteration(self):
        """
        Called from main loop, if your sink needs to handle GUI events
        do it here.

        Check any GUI flags then call Gtk.main_iteration to update things.
        """
        if self.show_vars:
            self.show_variables_window()
        else:
            self.hide_variables_window()

        for snapshot_f in self.scheduled_snapshots:
            fn = snapshot_f(self.last_draw_ctx)
            print("Saved snapshot: %s" % fn)
        else:
            self.scheduled_snapshots = deque()

        while Gtk.events_pending():
            Gtk.main_iteration()