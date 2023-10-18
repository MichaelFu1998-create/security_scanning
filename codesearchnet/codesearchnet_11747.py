def set_satchel_value(self, satchel, key, value):
        """
        Sets a key/value pair in a satchel's local renderer.
        """
        satchel = self.get_satchel(satchel)
        r = satchel.local_renderer
        setattr(r.env, key, value)
        print('Set %s=%s in satchel %s.' % (key, value, satchel.name))