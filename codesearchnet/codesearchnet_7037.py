def load_all_methods(self):
        r'''Method to load all data, and set all_methods based on the available
        data and properties. Demo function for testing only; must be
        implemented according to the methods available for each individual
        method.
        '''
        methods = []
        Tmins, Tmaxs = [], []
        if self.CASRN in ['7732-18-5', '67-56-1', '64-17-5']:
            methods.append(TEST_METHOD_1)
            self.TEST_METHOD_1_Tmin = 200.
            self.TEST_METHOD_1_Tmax = 350
            self.TEST_METHOD_1_coeffs = [1, .002]
            Tmins.append(self.TEST_METHOD_1_Tmin); Tmaxs.append(self.TEST_METHOD_1_Tmax)
        if self.CASRN in ['67-56-1']:
            methods.append(TEST_METHOD_2)
            self.TEST_METHOD_2_Tmin = 300.
            self.TEST_METHOD_2_Tmax = 400
            self.TEST_METHOD_2_coeffs = [1, .003]
            Tmins.append(self.TEST_METHOD_2_Tmin); Tmaxs.append(self.TEST_METHOD_2_Tmax)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin = min(Tmins)
            self.Tmax = max(Tmaxs)