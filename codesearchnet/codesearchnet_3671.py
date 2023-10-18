def train_encoder(X, y, fold_count, encoder):
    """
    Defines folds and performs the data preprocessing (categorical encoding, NaN imputation, normalization)
    Returns a list with {X_train, y_train, X_test, y_test}, average fit_encoder_time and average score_encoder_time

    Note: We normalize all features (not only numerical features) because otherwise SVM would
        get stuck for hours on ordinal encoded cylinder.bands.arff dataset due to presence of
        unproportionally high values.

    Note: The fold count is variable because there are datasets, which have less than 10 samples in the minority class.

    Note: We do not use pipelines because of:
        https://github.com/scikit-learn/scikit-learn/issues/11832
    """
    kf = StratifiedKFold(n_splits=fold_count, shuffle=True, random_state=2001)
    encoder = deepcopy(encoder)  # Because of https://github.com/scikit-learn-contrib/categorical-encoding/issues/106
    imputer = SimpleImputer(strategy='mean')
    scaler = StandardScaler()
    folds = []
    fit_encoder_time = 0
    score_encoder_time = 0

    for train_index, test_index in kf.split(X, y):
        # Split data
        X_train, X_test = X.iloc[train_index, :].reset_index(drop=True), X.iloc[test_index, :].reset_index(drop=True)
        y_train, y_test = y[train_index].reset_index(drop=True), y[test_index].reset_index(drop=True)

        # Training
        start_time = time.time()
        X_train = encoder.fit_transform(X_train, y_train)
        fit_encoder_time += time.time() - start_time
        X_train = imputer.fit_transform(X_train)
        X_train = scaler.fit_transform(X_train)

        # Testing
        start_time = time.time()
        X_test = encoder.transform(X_test)
        score_encoder_time += time.time() - start_time
        X_test = imputer.transform(X_test)
        X_test = scaler.transform(X_test)

        folds.append([X_train, y_train, X_test, y_test])

    return folds, fit_encoder_time/fold_count, score_encoder_time/fold_count