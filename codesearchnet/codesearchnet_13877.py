def load_profiles(self):
        """
        Loads all possible TUIO profiles and returns a dictionary with the
        profile addresses as keys and an instance of a profile as the value 
        """
        _profiles = {}
        for name, klass in inspect.getmembers(profiles):
            if inspect.isclass(klass) and name.endswith('Profile') and name != 'TuioProfile':
                # Adding profile to the self.profiles dictionary
                profile = klass()
                _profiles[profile.address] = profile
                # setting convenient variable to access objects of profile
                try:
                    setattr(self, profile.list_label, profile.objs)
                except AttributeError:
                    continue
                # Mapping callback method to every profile
                self.manager.add(self.callback, profile.address)
        return _profiles