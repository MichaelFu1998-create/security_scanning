def parse_doc (json_iter):
    """
    parse one document to prep for TextRank
    """
    global DEBUG

    for meta in json_iter:
        base_idx = 0

        for graf_text in filter_quotes(meta["text"], is_email=False):
            if DEBUG:
                print("graf_text:", graf_text)

            grafs, new_base_idx = parse_graf(meta["id"], graf_text, base_idx)
            base_idx = new_base_idx

            for graf in grafs:
                yield graf