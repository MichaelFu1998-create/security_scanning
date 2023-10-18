def train_rf_classifier(
        collected_features,
        test_fraction=0.25,
        n_crossval_iterations=20,
        n_kfolds=5,
        crossval_scoring_metric='f1',
        classifier_to_pickle=None,
        nworkers=-1,
):

    '''This gets the best RF classifier after running cross-validation.

    - splits the training set into test/train samples
    - does `KFold` stratified cross-validation using `RandomizedSearchCV`
    - gets the `RandomForestClassifier` with the best performance after CV
    - gets the confusion matrix for the test set

    Runs on the output dict from functions that produce dicts similar to that
    produced by `collect_nonperiodic_features` above.

    Parameters
    ----------

    collected_features : dict or str
        This is either the dict produced by a `collect_*_features` function or
        the pickle produced by the same.

    test_fraction : float
        This sets the fraction of the input set that will be used as the
        test set after training.

    n_crossval_iterations : int
        This sets the number of iterations to use when running the
        cross-validation.

    n_kfolds : int
        This sets the number of K-folds to use on the data when doing a
        test-train split.

    crossval_scoring_metric : str
        This is a string that describes how the cross-validation score is
        calculated for each iteration. See the URL below for how to specify this
        parameter:

        http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        By default, this is tuned for binary classification and uses the F1
        scoring metric. Change the `crossval_scoring_metric` to another metric
        (probably 'accuracy') for multi-class classification, e.g. for periodic
        variable classification.

    classifier_to_pickle : str
        If this is a string indicating the name of a pickle file to write, will
        write the trained classifier to the pickle that can be later loaded and
        used to classify data.

    nworkers : int
        This is the number of parallel workers to use in the
        RandomForestClassifier. Set to -1 to use all CPUs on your machine.

    Returns
    -------

    dict
        A dict containing the trained classifier, cross-validation results, the
        input data set, and all input kwargs used is returned, along with
        cross-validation score metrics.

    '''

    if (isinstance(collected_features,str) and
        os.path.exists(collected_features)):
        with open(collected_features,'rb') as infd:
            fdict = pickle.load(infd)
    elif isinstance(collected_features, dict):
        fdict = collected_features
    else:
        LOGERROR("can't figure out the input collected_features arg")
        return None

    tfeatures = fdict['features_array']
    tlabels = fdict['labels_array']
    tfeaturenames = fdict['availablefeatures']
    tmagcol = fdict['magcol']
    tobjectids = fdict['objectids']


    # split the training set into training/test samples using stratification
    # to keep the same fraction of variable/nonvariables in each
    training_features, testing_features, training_labels, testing_labels = (
        train_test_split(
            tfeatures,
            tlabels,
            test_size=test_fraction,
            random_state=RANDSEED,
            stratify=tlabels
        )
    )

    # get a random forest classifier
    clf = RandomForestClassifier(n_jobs=nworkers,
                                 random_state=RANDSEED)


    # this is the grid def for hyperparam optimization
    rf_hyperparams = {
        "max_depth": [3,4,5,None],
        "n_estimators":sp_randint(100,2000),
        "max_features": sp_randint(1, 5),
        "min_samples_split": sp_randint(2, 11),
        "min_samples_leaf": sp_randint(2, 11),
    }

    # run the stratified kfold cross-validation on training features using our
    # random forest classifier object
    cvsearch = RandomizedSearchCV(
        clf,
        param_distributions=rf_hyperparams,
        n_iter=n_crossval_iterations,
        scoring=crossval_scoring_metric,
        cv=StratifiedKFold(n_splits=n_kfolds,
                           shuffle=True,
                           random_state=RANDSEED),
        random_state=RANDSEED
    )


    LOGINFO('running grid-search CV to optimize RF hyperparameters...')
    cvsearch_classifiers = cvsearch.fit(training_features,
                                        training_labels)

    # report on the classifiers' performance
    _gridsearch_report(cvsearch_classifiers.cv_results_)

    # get the best classifier after CV is done
    bestclf = cvsearch_classifiers.best_estimator_
    bestclf_score = cvsearch_classifiers.best_score_
    bestclf_hyperparams = cvsearch_classifiers.best_params_

    # test this classifier on the testing set
    test_predicted_labels = bestclf.predict(testing_features)

    recscore = recall_score(testing_labels, test_predicted_labels)
    precscore = precision_score(testing_labels,test_predicted_labels)
    f1score = f1_score(testing_labels, test_predicted_labels)
    confmatrix = confusion_matrix(testing_labels, test_predicted_labels)

    # write the classifier, its training/testing set, and its stats to the
    # pickle if requested
    outdict = {'features':tfeatures,
               'labels':tlabels,
               'feature_names':tfeaturenames,
               'magcol':tmagcol,
               'objectids':tobjectids,
               'kwargs':{'test_fraction':test_fraction,
                         'n_crossval_iterations':n_crossval_iterations,
                         'n_kfolds':n_kfolds,
                         'crossval_scoring_metric':crossval_scoring_metric,
                         'nworkers':nworkers},
               'collect_kwargs':fdict['kwargs'],
               'testing_features':testing_features,
               'testing_labels':testing_labels,
               'training_features':training_features,
               'training_labels':training_labels,
               'best_classifier':bestclf,
               'best_score':bestclf_score,
               'best_hyperparams':bestclf_hyperparams,
               'best_recall':recscore,
               'best_precision':precscore,
               'best_f1':f1score,
               'best_confmatrix':confmatrix}


    if classifier_to_pickle:

        with open(classifier_to_pickle,'wb') as outfd:
            pickle.dump(outdict, outfd, pickle.HIGHEST_PROTOCOL)


    # return this classifier and accompanying info
    return outdict