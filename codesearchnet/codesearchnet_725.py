def evaluation(y_test=None, y_predict=None, n_classes=None):
    """
    Input the predicted results, targets results and
    the number of class, return the confusion matrix, F1-score of each class,
    accuracy and macro F1-score.

    Parameters
    ----------
    y_test : list
        The target results
    y_predict : list
        The predicted results
    n_classes : int
        The number of classes

    Examples
    --------
    >>> c_mat, f1, acc, f1_macro = tl.utils.evaluation(y_test, y_predict, n_classes)

    """
    c_mat = confusion_matrix(y_test, y_predict, labels=[x for x in range(n_classes)])
    f1 = f1_score(y_test, y_predict, average=None, labels=[x for x in range(n_classes)])
    f1_macro = f1_score(y_test, y_predict, average='macro')
    acc = accuracy_score(y_test, y_predict)
    tl.logging.info('confusion matrix: \n%s' % c_mat)
    tl.logging.info('f1-score        : %s' % f1)
    tl.logging.info('f1-score(macro) : %f' % f1_macro)  # same output with > f1_score(y_true, y_pred, average='macro')
    tl.logging.info('accuracy-score  : %f' % acc)
    return c_mat, f1, acc, f1_macro