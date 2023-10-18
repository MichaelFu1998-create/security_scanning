def aggregate_tree(l_tree):
    """Walk a py-radix tree and aggregate it.

    Arguments
    l_tree -- radix.Radix() object
    """

    def _aggregate_phase1(tree):
        # phase1 removes any supplied prefixes which are superfluous because
        # they are already included in another supplied prefix. For example,
        # 2001:67c:208c:10::/64 would be removed if 2001:67c:208c::/48 was
        # also supplied.
        n_tree = radix.Radix()
        for prefix in tree.prefixes():
            if tree.search_worst(prefix).prefix == prefix:
                n_tree.add(prefix)
        return n_tree

    def _aggregate_phase2(tree):
        # phase2 identifies adjacent prefixes that can be combined under a
        # single, shorter-length prefix. For example, 2001:67c:208c::/48 and
        # 2001:67c:208d::/48 can be combined into the single prefix
        # 2001:67c:208c::/47.
        n_tree = radix.Radix()
        for rnode in tree:
            p = text(ip_network(text(rnode.prefix)).supernet())
            r = tree.search_covered(p)
            if len(r) == 2:
                if r[0].prefixlen == r[1].prefixlen == rnode.prefixlen:
                    n_tree.add(p)
                else:
                    n_tree.add(rnode.prefix)
            else:
                n_tree.add(rnode.prefix)
        return n_tree

    l_tree = _aggregate_phase1(l_tree)

    if len(l_tree.prefixes()) == 1:
        return l_tree

    while True:
        r_tree = _aggregate_phase2(l_tree)
        if l_tree.prefixes() == r_tree.prefixes():
            break
        else:
            l_tree = r_tree
            del r_tree

    return l_tree