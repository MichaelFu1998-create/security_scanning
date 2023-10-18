def topological_order_packages(packages):
    """
    Order packages topologically.

    First returning packages which have message generators and then
    the rest based on all direct depends and indirect recursive run_depends.

    :param packages: A dict mapping relative paths to ``Package`` objects ``dict``
    :returns: A list of tuples containing the relative path and a ``Package`` object, ``list``
    """
    from catkin_pkg.topological_order import _PackageDecorator
    from catkin_pkg.topological_order import _sort_decorated_packages

    decorators_by_name = {}
    for path, package in packages.items():
        decorators_by_name[package.name] = _PackageDecorator(package, path)

    # calculate transitive dependencies
    for decorator in decorators_by_name.values():
        decorator.depends_for_topological_order = set([])
        all_depends = \
            decorator.package.build_depends + decorator.package.buildtool_depends + \
            decorator.package.run_depends + decorator.package.test_depends
        # skip external dependencies, meaning names that are not known packages
        unique_depend_names = set([
            d.name for d in all_depends if d.name in decorators_by_name.keys()])
        for name in unique_depend_names:
            if name in decorator.depends_for_topological_order:
                # avoid function call to improve performance
                # check within the loop since the set changes every cycle
                continue
            decorators_by_name[name]._add_recursive_run_depends(
                decorators_by_name, decorator.depends_for_topological_order)

    ordered_pkg_tuples = _sort_decorated_packages(decorators_by_name)
    for pkg_path, pkg in ordered_pkg_tuples:
        if pkg_path is None:
            raise RuntimeError('Circular dependency in: %s' % pkg)
    return ordered_pkg_tuples