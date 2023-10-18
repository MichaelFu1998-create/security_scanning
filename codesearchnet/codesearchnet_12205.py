def apply_rf_classifier(classifier,
                        varfeaturesdir,
                        outpickle,
                        maxobjects=None):
    '''This applys an RF classifier trained using `train_rf_classifier`
    to varfeatures pickles in `varfeaturesdir`.

    Parameters
    ----------

    classifier : dict or str
        This is the output dict or pickle created by `get_rf_classifier`. This
        will contain a `features_name` key that will be used to collect the same
        features used to train the classifier from the varfeatures pickles in
        varfeaturesdir.

    varfeaturesdir : str
        The directory containing the varfeatures pickles for objects that will
        be classified by the trained `classifier`.

    outpickle : str
        This is a filename for the pickle that will be written containing the
        result dict from this function.

    maxobjects : int
        This sets the number of objects to process in `varfeaturesdir`.

    Returns
    -------

    dict
        The classification results after running the trained `classifier` as
        returned as a dict. This contains predicted labels and their prediction
        probabilities.

    '''

    if isinstance(classifier,str) and os.path.exists(classifier):
        with open(classifier,'rb') as infd:
            clfdict = pickle.load(infd)
    elif isinstance(classifier, dict):
        clfdict = classifier
    else:
        LOGERROR("can't figure out the input classifier arg")
        return None


    # get the features to extract from clfdict
    if 'feature_names' not in clfdict:
        LOGERROR("feature_names not present in classifier input, "
                 "can't figure out which ones to extract from "
                 "varfeature pickles in %s" % varfeaturesdir)
        return None

    # get the feature labeltype, pklglob, and maxobjects from classifier's
    # collect_kwargs elem.
    featurestouse = clfdict['feature_names']
    pklglob = clfdict['collect_kwargs']['pklglob']
    magcol = clfdict['magcol']


    # extract the features used by the classifier from the varfeatures pickles
    # in varfeaturesdir using the pklglob provided
    featfile = os.path.join(
        os.path.dirname(outpickle),
        'actual-collected-features.pkl'
    )

    features = collect_nonperiodic_features(
        varfeaturesdir,
        magcol,
        featfile,
        pklglob=pklglob,
        featurestouse=featurestouse,
        maxobjects=maxobjects
    )

    # now use the trained classifier on these features
    bestclf = clfdict['best_classifier']

    predicted_labels = bestclf.predict(features['features_array'])

    # FIXME: do we need to use the probability calibration curves to fix these
    # probabilities? probably. figure out how to do this.
    predicted_label_probs = bestclf.predict_proba(
        features['features_array']
    )

    outdict = {
        'features':features,
        'featfile':featfile,
        'classifier':clfdict,
        'predicted_labels':predicted_labels,
        'predicted_label_probs':predicted_label_probs,
    }

    with open(outpickle,'wb') as outfd:
        pickle.dump(outdict, outfd, pickle.HIGHEST_PROTOCOL)

    return outdict