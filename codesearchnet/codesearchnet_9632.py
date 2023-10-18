def _shift_required(tiles):
    """Determine if distance over antimeridian is shorter than normal distance."""
    if tiles[0][0].tile_pyramid.is_global:
        # get set of tile columns
        tile_cols = sorted(list(set([t[0].col for t in tiles])))
        # if tile columns are an unbroken sequence, tiles are connected and are not
        # passing the Antimeridian
        if tile_cols == list(range(min(tile_cols), max(tile_cols) + 1)):
            return False
        else:
            # look at column gaps and try to determine the smallest distance
            def gen_groups(items):
                """Groups tile columns by sequence."""
                j = items[0]
                group = [j]
                for i in items[1:]:
                    # item is next in expected sequence
                    if i == j + 1:
                        group.append(i)
                    # gap occured, so yield existing group and create new one
                    else:
                        yield group
                        group = [i]
                    j = i
                yield group

            groups = list(gen_groups(tile_cols))
            # in case there is only one group, don't shift
            if len(groups) == 1:
                return False
            # distance between first column of first group and last column of last group
            normal_distance = groups[-1][-1] - groups[0][0]
            # distance between last column of first group and last column of first group
            # but crossing the antimeridian
            antimeridian_distance = (
                groups[0][-1] + tiles[0][0].tile_pyramid.matrix_width(tiles[0][0].zoom)
            ) - groups[-1][0]
            # return whether distance over antimeridian is shorter
            return antimeridian_distance < normal_distance
    else:
        return False