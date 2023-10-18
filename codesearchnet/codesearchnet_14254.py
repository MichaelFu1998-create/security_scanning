def get_key_map(self):
        '''
        Return a dict in the form of

        SHOEBOT_KEY_NAME, GTK_VALUE

        Shoebot key names look like KEY_LEFT, whereas Gdk uses KEY_Left
        - Shoebot key names are derived from Nodebox 1, which was a mac
          app.
        '''
        kdict = {}
        for gdk_name in dir(Gdk):
            nb_name = gdk_name.upper()
            kdict[nb_name] = getattr(Gdk, gdk_name)
        return kdict