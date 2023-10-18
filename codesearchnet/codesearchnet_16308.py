def iteration(self):
        """
        Runs the ipfn algorithm. Automatically detects of working with numpy ndarray or pandas dataframes.
        """

        i = 0
        conv = np.inf
        old_conv = -np.inf
        conv_list = []
        m = self.original

        # If the original data input is in pandas DataFrame format
        if isinstance(self.original, pd.DataFrame):
            ipfn_method = self.ipfn_df
        elif isinstance(self.original, np.ndarray):
            ipfn_method = self.ipfn_np
            self.original = self.original.astype('float64')
        else:
            print('Data input instance not recognized')
            sys.exit(0)
        while ((i <= self.max_itr and conv > self.conv_rate) and
               (i <= self.max_itr and abs(conv - old_conv) > self.rate_tolerance)):
            old_conv = conv
            m, conv = ipfn_method(m, self.aggregates, self.dimensions, self.weight_col)
            conv_list.append(conv)
            i += 1
        converged = 1
        if i <= self.max_itr:
            if not conv > self.conv_rate:
                print('ipfn converged: convergence_rate below threshold')
            elif not abs(conv - old_conv) > self.rate_tolerance:
                print('ipfn converged: convergence_rate not updating or below rate_tolerance')
        else:
            print('Maximum iterations reached')
            converged = 0

        # Handle the verbose
        if self.verbose == 0:
            return m
        elif self.verbose == 1:
            return m, converged
        elif self.verbose == 2:
            return m, converged, pd.DataFrame({'iteration': range(i), 'conv': conv_list}).set_index('iteration')
        else:
            print('wrong verbose input, return None')
            sys.exit(0)