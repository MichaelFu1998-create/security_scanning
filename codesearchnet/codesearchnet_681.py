def tsne_embedding(embeddings, reverse_dictionary, plot_only=500, second=5, saveable=False, name='tsne', fig_idx=9862):
    """Visualize the embeddings by using t-SNE.

    Parameters
    ----------
    embeddings : numpy.array
        The embedding matrix.
    reverse_dictionary : dictionary
        id_to_word, mapping id to unique word.
    plot_only : int
        The number of examples to plot, choice the most common words.
    second : int
        The display second(s) for the image(s), if saveable is False.
    saveable : boolean
        Save or plot the figure.
    name : str
        A name to save the image, if saveable is True.
    fig_idx : int
        matplotlib figure index.

    Examples
    --------
    >>> see 'tutorial_word2vec_basic.py'
    >>> final_embeddings = normalized_embeddings.eval()
    >>> tl.visualize.tsne_embedding(final_embeddings, labels, reverse_dictionary,
    ...                   plot_only=500, second=5, saveable=False, name='tsne')

    """
    import matplotlib.pyplot as plt

    def plot_with_labels(low_dim_embs, labels, figsize=(18, 18), second=5, saveable=True, name='tsne', fig_idx=9862):

        if low_dim_embs.shape[0] < len(labels):
            raise AssertionError("More labels than embeddings")

        if saveable is False:
            plt.ion()
            plt.figure(fig_idx)

        plt.figure(figsize=figsize)  # in inches

        for i, label in enumerate(labels):
            x, y = low_dim_embs[i, :]
            plt.scatter(x, y)
            plt.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')

        if saveable:
            plt.savefig(name + '.pdf', format='pdf')
        else:
            plt.draw()
            plt.pause(second)

    try:
        from sklearn.manifold import TSNE
        from six.moves import xrange

        tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
        # plot_only = 500
        low_dim_embs = tsne.fit_transform(embeddings[:plot_only, :])
        labels = [reverse_dictionary[i] for i in xrange(plot_only)]
        plot_with_labels(low_dim_embs, labels, second=second, saveable=saveable, name=name, fig_idx=fig_idx)

    except ImportError:
        _err = "Please install sklearn and matplotlib to visualize embeddings."
        tl.logging.error(_err)
        raise ImportError(_err)