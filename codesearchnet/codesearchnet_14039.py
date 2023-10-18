def gtk_mouse_button_down(self, widget, event):
        ''' Handle right mouse button clicks '''
        if self.menu_enabled and event.button == 3:
            menu = self.uimanager.get_widget('/Save as')
            menu.popup(None, None, None, None, event.button, event.time)
        else:
            super(ShoebotWindow, self).gtk_mouse_button_down(widget, event)