def load_and_preprocess_imdb_data(n_gram=None):
    """Load IMDb data and augment with hashed n-gram features."""
    X_train, y_train, X_test, y_test = tl.files.load_imdb_dataset(nb_words=VOCAB_SIZE)

    if n_gram is not None:
        X_train = np.array([augment_with_ngrams(x, VOCAB_SIZE, N_BUCKETS, n=n_gram) for x in X_train])
        X_test = np.array([augment_with_ngrams(x, VOCAB_SIZE, N_BUCKETS, n=n_gram) for x in X_test])

    return X_train, y_train, X_test, y_test