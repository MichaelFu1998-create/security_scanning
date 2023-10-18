def add_event_callback(self, pin, callback, bouncetime=-1):
        """Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        kwargs = {}
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self.bbio_gpio.add_event_callback(pin, callback, **kwargs)