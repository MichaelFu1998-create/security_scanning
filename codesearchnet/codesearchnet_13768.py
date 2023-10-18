def summarize(text, sent_limit=None, char_limit=None, imp_require=None,
              debug=False, **lexrank_params):
    '''
    Args:
      text: text to be summarized (unicode string)
      sent_limit: summary length (the number of sentences)
      char_limit: summary length (the number of characters)
      imp_require: cumulative LexRank score [0.0-1.0]

    Returns:
      list of extracted sentences
    '''
    debug_info = {}
    sentences = list(tools.sent_splitter_ja(text))
    scores, sim_mat = lexrank(sentences, **lexrank_params)
    sum_scores = sum(scores.itervalues())
    acc_scores = 0.0
    indexes = set()
    num_sent, num_char = 0, 0
    for i in sorted(scores, key=lambda i: scores[i], reverse=True):
        num_sent += 1
        num_char += len(sentences[i])
        if sent_limit is not None and num_sent > sent_limit:
            break
        if char_limit is not None and num_char > char_limit:
            break
        if imp_require is not None and acc_scores / sum_scores >= imp_require:
            break
        indexes.add(i)
        acc_scores += scores[i]

    if len(indexes) > 0:
        summary_sents = [sentences[i] for i in sorted(indexes)]
    else:
        summary_sents = sentences

    if debug:
        debug_info.update({
            'sentences': sentences, 'scores': scores
        })

    return summary_sents, debug_info