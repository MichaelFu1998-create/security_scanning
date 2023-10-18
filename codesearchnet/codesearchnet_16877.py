def _process_tabs(self, tabs, current_tab, group_current_tab):
        """
        Process and prepare tabs.

        This includes steps like updating references to the current tab,
        filtering out hidden tabs, sorting tabs etc...

        Args:
            tabs:
                The list of tabs to process.
            current_tab:
                The reference to the currently loaded tab.
            group_current_tab:
                The reference to the active tab in the current tab group. For
                parent tabs, this is different than for the current tab group.

        Returns:
            Processed list of tabs. Note that the method may have side effects.

        """
        # Update references to the current tab
        for t in tabs:
            t.current_tab = current_tab
            t.group_current_tab = group_current_tab

        # Filter out hidden tabs
        tabs = list(filter(lambda t: t.tab_visible, tabs))

        # Sort remaining tabs in-place
        tabs.sort(key=lambda t: t.weight)

        return tabs