def _menuItem(self, menuitem, *args):
        """Return the specified menu item.

        Example - refer to items by name:

        app._menuItem(app.AXMenuBar, 'File', 'New').Press()
        app._menuItem(app.AXMenuBar, 'Edit', 'Insert', 'Line Break').Press()

        Refer to items by index:

        app._menuitem(app.AXMenuBar, 1, 0).Press()

        Refer to items by mix-n-match:

        app._menuitem(app.AXMenuBar, 1, 'About TextEdit').Press()
        """
        self._activate()
        for item in args:
            # If the item has an AXMenu as a child, navigate into it.
            # This seems like a silly abstraction added by apple's a11y api.
            if menuitem.AXChildren[0].AXRole == 'AXMenu':
                menuitem = menuitem.AXChildren[0]
            # Find AXMenuBarItems and AXMenuItems using a handy wildcard
            role = 'AXMenu*Item'
            try:
                menuitem = menuitem.AXChildren[int(item)]
            except ValueError:
                menuitem = menuitem.findFirst(AXRole='AXMenu*Item',
                                              AXTitle=item)
        return menuitem