def get_cv_error(clf,feats,scores):
    """
    Gets cross validated error for a given classifier, set of features, and scores
    clf - classifier
    feats - features to feed into the classified and cross validate over
    scores - scores associated with the features -- feature row 1 associates with score 1, etc.
    """
    results={'success' : False, 'kappa' : 0, 'mae' : 0}
    try:
        cv_preds=util_functions.gen_cv_preds(clf,feats,scores)
        err=numpy.mean(numpy.abs(numpy.array(cv_preds)-scores))
        kappa=util_functions.quadratic_weighted_kappa(list(cv_preds),scores)
        results['mae']=err
        results['kappa']=kappa
        results['success']=True
    except ValueError as ex:
        # If this is hit, everything is fine.  It is hard to explain why the error occurs, but it isn't a big deal.
        msg = u"Not enough classes (0,1,etc) in each cross validation fold: {ex}".format(ex=ex)
        log.debug(msg)
    except:
        log.exception("Error getting cv error estimates.")

    return results