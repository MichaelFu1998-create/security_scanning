def main(loader, name):
    """
    Here we iterate through the datasets and score them with a classifier using different encodings.

    """

    scores = []
    raw_scores_ds = {}

    # first get the dataset
    X, y, mapping = loader()

    clf = linear_model.LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=200, random_state=0)

    # try each encoding method available, which works on multiclass problems
    encoders = (set(category_encoders.__all__) - {'WOEEncoder'})  # WoE is currently only for binary targets

    for encoder_name in encoders:
        encoder = getattr(category_encoders, encoder_name)
        start_time = time.time()
        score, stds, raw_scores, dim = score_models(clf, X, y, encoder)
        scores.append([encoder_name, name, dim, score, stds, time.time() - start_time])
        raw_scores_ds[encoder_name] = raw_scores
        gc.collect()

    results = pd.DataFrame(scores, columns=['Encoding', 'Dataset', 'Dimensionality', 'Avg. Score', 'Score StDev', 'Elapsed Time'])

    raw = pd.DataFrame.from_dict(raw_scores_ds)
    ax = raw.plot(kind='box', return_type='axes')
    plt.title('Scores for Encodings on %s Dataset' % (name,))
    plt.ylabel('Score (higher is better)')
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    plt.grid()
    plt.tight_layout()
    plt.show()

    return results, raw