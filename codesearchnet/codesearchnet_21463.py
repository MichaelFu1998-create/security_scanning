def traverse(element, query, deep=False):
    """
    Helper function to traverse an element tree rooted at element, yielding nodes matching the query.
    """
    # Grab the next part of the query (it will be chopped from the front each iteration).
    part = query[0]
    if not part:
        # If the part is blank, we encountered a //, meaning search all sub-nodes.
        query = query[1:]
        part = query[0]
        deep = True
    # Parse out any predicate (tag[pred]) from this part of the query.
    part, predicate = xpath_re.match(query[0]).groups()
    for c in element._children:
        if part in ('*', c.tagname) and c._match(predicate):
            # A potential matching branch: this child matches the next query part (and predicate).
            if len(query) == 1:
                # If this is the last part of the query, we found a matching element, yield it.
                yield c
            else:
                # Otherwise, check the children of this child against the next query part.
                for e in traverse(c, query[1:]):
                    yield e
        if deep:
            # If we're searching all sub-nodes, traverse with the same query, regardless of matching.
            # This basically creates a recursion branch to search EVERYWHERE for anything after //.
            for e in traverse(c, query, deep=True):
                yield e