def gen_preds(clf, arr):
    """
    Generates predictions on a novel data array using a fit classifier
    clf is a classifier that has already been fit
    arr is a data array identical in dimension to the array clf was trained on
    Returns the array of predictions.
    """
    if(hasattr(clf, "predict_proba")):
        ret = clf.predict(arr)
        # pred_score=preds.argmax(1)+min(x._score)
    else:
        ret = clf.predict(arr)
    return ret