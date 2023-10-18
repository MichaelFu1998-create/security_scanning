def train_model(folds, model):
    """
    Evaluation with:
      Matthews correlation coefficient: represents thresholding measures
      AUC: represents ranking measures
      Brier score: represents calibration measures
    """
    scores = []
    fit_model_time = 0      # Sum of all the time spend on fitting the training data, later on normalized
    score_model_time = 0    # Sum of all the time spend on scoring the testing data, later on normalized

    for X_train, y_train, X_test, y_test in folds:
        # Training
        start_time = time.time()
        with ignore_warnings(category=ConvergenceWarning):  # Yes, neural networks do not always converge
            model.fit(X_train, y_train)
        fit_model_time += time.time() - start_time
        prediction_train_proba = model.predict_proba(X_train)[:, 1]
        prediction_train = (prediction_train_proba >= 0.5).astype('uint8')

        # Testing
        start_time = time.time()
        prediction_test_proba = model.predict_proba(X_test)[:, 1]
        score_model_time += time.time() - start_time
        prediction_test = (prediction_test_proba >= 0.5).astype('uint8')

        # When all the predictions are of a single class, we get a RuntimeWarning in matthews_corr
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            scores.append([
                sklearn.metrics.matthews_corrcoef(y_test, prediction_test),
                sklearn.metrics.matthews_corrcoef(y_train, prediction_train),
                sklearn.metrics.roc_auc_score(y_test, prediction_test_proba),
                sklearn.metrics.roc_auc_score(y_train, prediction_train_proba),
                sklearn.metrics.brier_score_loss(y_test, prediction_test_proba),
                sklearn.metrics.brier_score_loss(y_train, prediction_train_proba)
            ])

    return np.mean(scores, axis=0), fit_model_time/len(folds), score_model_time/len(folds)