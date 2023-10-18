def _check_groups(s, groups):
    """Ensures that all particles are included in exactly 1 group"""
    ans = []
    for g in groups:
        ans.extend(g)
    if np.unique(ans).size != np.size(ans):
        return False
    elif np.unique(ans).size != s.obj_get_positions().shape[0]:
        return False
    else:
        return (np.arange(s.obj_get_radii().size) == np.sort(ans)).all()