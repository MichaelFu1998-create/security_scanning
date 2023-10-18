def evaluate(best_processed_path, model):
    """
    Evaluate model on splitted 10 percent testing set
    """
    x_test_char, x_test_type, y_test = prepare_feature(best_processed_path, option='test')

    y_predict = model.predict([x_test_char, x_test_type])
    y_predict = (y_predict.ravel() > 0.5).astype(int)

    f1score = f1_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)

    return f1score, precision, recall