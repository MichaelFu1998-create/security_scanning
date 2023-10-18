def ipfn_df(self, df, aggregates, dimensions, weight_col='total'):
        """
        Runs the ipfn method from a dataframe df, aggregates/marginals and the dimension(s) preserved.
        For example:
        from ipfn import ipfn
        import pandas as pd
        age = [30, 30, 30, 30, 40, 40, 40, 40, 50, 50, 50, 50]
        distance = [10,20,30,40,10,20,30,40,10,20,30,40]
        m = [8., 4., 6., 7., 3., 6., 5., 2., 9., 11., 3., 1.]
        df = pd.DataFrame()
        df['age'] = age
        df['distance'] = distance
        df['total'] = m

        xip = df.groupby('age')['total'].sum()
        xip.loc[30] = 20
        xip.loc[40] = 18
        xip.loc[50] = 22
        xpj = df.groupby('distance')['total'].sum()
        xpj.loc[10] = 18
        xpj.loc[20] = 16
        xpj.loc[30] = 12
        xpj.loc[40] = 14
        dimensions = [['age'], ['distance']]
        aggregates = [xip, xpj]

        IPF = ipfn(df, aggregates, dimensions)
        df = IPF.iteration()

        print(df)
        print(df.groupby('age')['total'].sum(), xip)"""

        steps = len(aggregates)
        tables = [df]
        for inc in range(steps - 1):
            tables.append(df.copy())
        original = df.copy()

        # Calculate the new weights for each dimension
        inc = 0
        for features in dimensions:
            if inc == (steps - 1):
                table_update = df
                table_current = tables[inc]
            else:
                table_update = tables[inc + 1]
                table_current = tables[inc]

            tmp = table_current.groupby(features)[weight_col].sum()
            xijk = aggregates[inc]

            feat_l = []
            for feature in features:
                feat_l.append(np.unique(table_current[feature]))
            table_update.set_index(features, inplace=True)
            table_current.set_index(features, inplace=True)

            for feature in product(*feat_l):
                den = tmp.loc[feature]
                # calculate new weight for this iteration
                if den == 0:
                    table_update.loc[feature, weight_col] =\
                        table_current.loc[feature, weight_col] *\
                        xijk.loc[feature]
                else:
                    table_update.loc[feature, weight_col] = \
                        table_current.loc[feature, weight_col].astype(float) * \
                        xijk.loc[feature] / den

            table_update.reset_index(inplace=True)
            table_current.reset_index(inplace=True)
            inc += 1
            feat_l = []

        # Calculate the max convergence rate
        max_conv = 0
        inc = 0
        for features in dimensions:
            tmp = df.groupby(features)[weight_col].sum()
            ori_ijk = aggregates[inc]
            temp_conv = max(abs(tmp / ori_ijk - 1))
            if temp_conv > max_conv:
                max_conv = temp_conv
            inc += 1

        return df, max_conv