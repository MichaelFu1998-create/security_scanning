def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        x = state['x']

        # create the slag constituent categories
        compounds_sio2 = ['SiO2', 'PO2.5', 'TiO2', 'ZrO2']
        compounds_cao = ['CaO', 'MgO', 'FeO1.5', 'FeO', 'MnO', 'BO1.5']
        compounds_al2o3 = ['Al2O3']
        compounds_caf2 = ['CaF2']
        compounds_na2o = ['Na2O', 'K2O']
        compounds_all = (compounds_sio2 + compounds_cao + compounds_al2o3 +
                         compounds_caf2 + compounds_na2o)

        # convert compounds with two cations to single cation equivalents
        if 'P2O5' in x:
            x['PO2.5'] = 2.0 * x['P2O5']
        if 'Fe2O3' in x:
            x['FeO1.5'] = 2.0 * x['Fe2O3']
        if 'B2O3' in x:
            x['BO1.5'] = 2.0 * x['B2O3']

        # normalise mole fractions, use only compounds in compounds_all
        x_total = sum([x.get(c, 0.0) for c in compounds_all])
        x = {c: x.get(c, 0.0)/x_total for c in compounds_all}

        # calculate the cateogry mole fractions
        x1 = sum([x.get(c, 0.0) for c in compounds_sio2])
        x2 = sum([x.get(c, 0.0) for c in compounds_cao])
        x3 = sum([x.get(c, 0.0) for c in compounds_al2o3])
        x4 = sum([x.get(c, 0.0) for c in compounds_caf2])
        x5 = sum([x.get(c, 0.0) for c in compounds_na2o])

        # TODO: Why is x1 not used? This looks suspicious.
        A = exp(-17.51 + 1.73*x2 + 5.82*x4 + 7.02*x5 - 33.76*x3)
        B = 31140.0 - 23896.0*x2 - 46356.0*x4 - 39159.0*x5 + 68833.0*x3

        result = A*T*exp(B/T)  # [P]

        return result / 10.0