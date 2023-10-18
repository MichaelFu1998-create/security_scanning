def cds_score(self, x_te, y_te):
        """ Computes the cds statistic from variable 1 to variable 2

        Args:
            x_te (numpy.ndarray): Variable 1
            y_te (numpy.ndarray): Variable 2

        Returns:
            float: CDS fit score
        """
        if type(x_te) == np.ndarray:
            x_te, y_te = pd.Series(x_te.reshape(-1)), pd.Series(y_te.reshape(-1))
        xd, yd = discretized_sequences(x_te,  y_te,  self.ffactor, self.maxdev)
        cx = Counter(xd)
        cy = Counter(yd)
        yrange = sorted(cy.keys())
        ny = len(yrange)
        py = np.array([cy[i] for i in yrange], dtype=float)
        py = py / py.sum()
        pyx = []
        for a in cx:
            if cx[a] > self.minc:
                yx = y_te[xd == a]
                # if not numerical(ty):
                #     cyx = Counter(yx)
                #     pyxa = np.array([cyx[i] for i in yrange], dtype=float)
                #     pyxa.sort()
                if count_unique(y_te) > len_discretized_values(y_te, "Numerical", self.ffactor, self.maxdev):

                    yx = (yx - np.mean(yx)) / np.std(y_te)
                    yx = discretized_sequence(yx, "Numerical", self.ffactor, self.maxdev, norm=False)
                    cyx = Counter(yx.astype(int))
                    pyxa = np.array([cyx[i] for i in discretized_values(y_te, "Numerical", self.ffactor, self.maxdev)],
                                    dtype=float)

                else:
                    cyx = Counter(yx)
                    pyxa = [cyx[i] for i in yrange]
                    pyxax = np.array([0] * (ny - 1) + pyxa + [0] * (ny - 1), dtype=float)
                    xcorr = [sum(py * pyxax[i:i + ny]) for i in range(2 * ny - 1)]
                    imax = xcorr.index(max(xcorr))
                    pyxa = np.array([0] * (2 * ny - 2 - imax) + pyxa + [0] * imax, dtype=float)
                assert pyxa.sum() == cx[a]
                pyxa = pyxa / pyxa.sum()

                pyx.append(pyxa)

        if len(pyx) == 0:
            return 0

        pyx = np.array(pyx)
        pyx = pyx - pyx.mean(axis=0)
        return np.std(pyx)