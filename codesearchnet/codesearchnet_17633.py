def create(dataset, symbol, degree):
        """
        Create a model object from the data set for the property specified by
        the supplied symbol, using the specified polynomial degree.

        :param dataset: a DataSet object
        :param symbol: the symbol of the property to be described, e.g. 'rho'
        :param degree: the polynomial degree to use

        :returns: a new PolynomialModelT object
        """

        x_vals = dataset.data['T'].tolist()
        y_vals = dataset.data[symbol].tolist()
        coeffs = np.polyfit(x_vals, y_vals, degree)

        result = PolynomialModelT(dataset.material,
                                  dataset.names_dict[symbol],
                                  symbol, dataset.display_symbols_dict[symbol],
                                  dataset.units_dict[symbol],
                                  None, [dataset.name], coeffs)

        result.state_schema['T']['min'] = float(min(x_vals))
        result.state_schema['T']['max'] = float(max(x_vals))

        return result