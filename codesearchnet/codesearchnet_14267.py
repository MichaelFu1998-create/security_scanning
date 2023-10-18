def widget_changed(self, widget, v):
        ''' Called when a slider is adjusted. '''
        # set the appropriate bot var
        if v.type is NUMBER:
            self.bot._namespace[v.name] = widget.get_value()
            self.bot._vars[v.name].value = widget.get_value()  ## Not sure if this is how to do this - stu
            publish_event(VARIABLE_UPDATED_EVENT, v)  # pretty dumb for now
        elif v.type is BOOLEAN:
            self.bot._namespace[v.name] = widget.get_active()
            self.bot._vars[v.name].value = widget.get_active()  ## Not sure if this is how to do this - stu
            publish_event(VARIABLE_UPDATED_EVENT, v)  # pretty dumb for now
        elif v.type is TEXT:
            self.bot._namespace[v.name] = widget.get_text()
            self.bot._vars[v.name].value = widget.get_text()  ## Not sure if this is how to do this - stu
            publish_event(VARIABLE_UPDATED_EVENT, v)