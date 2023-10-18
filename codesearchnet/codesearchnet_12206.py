def plot_training_results(classifier,
                          classlabels,
                          outfile):
    '''This plots the training results from the classifier run on the training
    set.

    - plots the confusion matrix

    - plots the feature importances

    - FIXME: plot the learning curves too, see:
      http://scikit-learn.org/stable/modules/learning_curve.html

    Parameters
    ----------

    classifier : dict or str
        This is the output dict or pickle created by `get_rf_classifier`
        containing the trained classifier.

    classlabels : list of str
        This contains all of the class labels for the current classification
        problem.

    outfile : str
        This is the filename where the plots will be written.

    Returns
    -------

    str
        The path to the generated plot file.

    '''

    if isinstance(classifier,str) and os.path.exists(classifier):
        with open(classifier,'rb') as infd:
            clfdict = pickle.load(infd)
    elif isinstance(classifier, dict):
        clfdict = classifier
    else:
        LOGERROR("can't figure out the input classifier arg")
        return None

    confmatrix = clfdict['best_confmatrix']
    overall_feature_importances = clfdict[
        'best_classifier'
    ].feature_importances_
    feature_importances_per_tree = np.array([
        tree.feature_importances_
        for tree in clfdict['best_classifier'].estimators_
    ])
    stdev_feature_importances = np.std(feature_importances_per_tree,axis=0)

    feature_names = np.array(clfdict['feature_names'])

    plt.figure(figsize=(6.4*3.0,4.8))

    # confusion matrix
    plt.subplot(121)
    classes = np.array(classlabels)
    plt.imshow(confmatrix, interpolation='nearest', cmap=plt.cm.Blues)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    plt.title('evaluation set confusion matrix')
    plt.ylabel('predicted class')
    plt.xlabel('actual class')

    thresh = confmatrix.max() / 2.
    for i, j in itertools.product(range(confmatrix.shape[0]),
                                  range(confmatrix.shape[1])):
        plt.text(j, i, confmatrix[i, j],
                 horizontalalignment="center",
                 color="white" if confmatrix[i, j] > thresh else "black")

    # feature importances
    plt.subplot(122)

    features = np.array(feature_names)
    sorted_ind = np.argsort(overall_feature_importances)[::-1]

    features = features[sorted_ind]
    feature_names = feature_names[sorted_ind]
    overall_feature_importances = overall_feature_importances[sorted_ind]
    stdev_feature_importances = stdev_feature_importances[sorted_ind]

    plt.bar(np.arange(0,features.size),
            overall_feature_importances,
            yerr=stdev_feature_importances,
            width=0.8,
            color='grey')
    plt.xticks(np.arange(0,features.size),
               features,
               rotation=90)
    plt.yticks([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    plt.xlim(-0.75, features.size - 1.0 + 0.75)
    plt.ylim(0.0,0.9)
    plt.ylabel('relative importance')
    plt.title('relative importance of features')

    plt.subplots_adjust(wspace=0.1)

    plt.savefig(outfile,
                bbox_inches='tight',
                dpi=100)
    plt.close('all')
    return outfile