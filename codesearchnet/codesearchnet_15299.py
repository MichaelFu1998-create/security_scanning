def get_modules() -> Mapping:
    """Get all Bio2BEL modules."""
    modules = {}

    for entry_point in iter_entry_points(group='bio2bel', name=None):
        entry = entry_point.name

        try:
            modules[entry] = entry_point.load()
        except VersionConflict as exc:
            log.warning('Version conflict in %s: %s', entry, exc)
            continue
        except UnknownExtra as exc:
            log.warning('Unknown extra in %s: %s', entry, exc)
            continue
        except ImportError as exc:
            log.exception('Issue with importing module %s: %s', entry, exc)
            continue

    return modules