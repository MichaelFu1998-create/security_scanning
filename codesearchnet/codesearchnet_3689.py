def convert_input(X):
    """
    Unite data into a DataFrame.
    """
    if not isinstance(X, pd.DataFrame):
        if isinstance(X, list):
            X = pd.DataFrame(X)
        elif isinstance(X, (np.generic, np.ndarray)):
            X = pd.DataFrame(X)
        elif isinstance(X, csr_matrix):
            X = pd.DataFrame(X.todense())
        elif isinstance(X, pd.Series):
            X = pd.DataFrame(X)
        else:
            raise ValueError('Unexpected input type: %s' % (str(type(X))))

        X = X.apply(lambda x: pd.to_numeric(x, errors='ignore'))

    return X