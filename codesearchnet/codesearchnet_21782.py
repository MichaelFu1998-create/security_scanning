def fullStats(a, b):
    """Performs several stats on a against b, typically a is the predictions
    array, and b the observations array

    Returns:
        A dataFrame of stat name, stat description, result
    """

    stats = [
        ['bias', 'Bias', bias(a, b)],
        ['stderr', 'Standard Deviation Error', stderr(a, b)],
        ['mae', 'Mean Absolute Error', mae(a, b)],
        ['rmse', 'Root Mean Square Error', rmse(a, b)],
        ['nmse', 'Normalized Mean Square Error', nmse(a, b)],
        ['mfbe', 'Mean Fractionalized bias Error', mfbe(a, b)],
        ['fa2', 'Factor of Two', fa(a, b, 2)],
        ['foex', 'Factor of Exceedance', foex(a, b)],
        ['correlation', 'Correlation R', correlation(a, b)],
        ['determination', 'Coefficient of Determination r2', determination(a, b)],
        ['gmb', 'Geometric Mean Bias', gmb(a, b)],
        ['gmv', 'Geometric Mean Variance', gmv(a, b)],
        ['fmt', 'Figure of Merit in Time', fmt(a, b)]
    ]
    rec = np.rec.fromrecords(stats, names=('stat', 'description', 'result'))
    df = pd.DataFrame.from_records(rec, index='stat')
    return df