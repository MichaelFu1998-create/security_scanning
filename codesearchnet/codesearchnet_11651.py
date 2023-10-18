def baseTargetSpec(self):
        ''' returns pack.DependencySpec for the base target of this target (or
            None if this target does not inherit from another target.
        '''
        inherits = self.description.get('inherits', {})
        if len(inherits) == 1:
            name, version_req = list(inherits.items())[0]
            shrinkwrap_version_req = self.getShrinkwrapMapping('targets').get(name, None)
            if shrinkwrap_version_req is not None:
                logger.debug(
                    'respecting shrinkwrap version %s for %s', shrinkwrap_version_req, name
                )
            return pack.DependencySpec(
                name,
                version_req,
                shrinkwrap_version_req = shrinkwrap_version_req
            )
        elif len(inherits) > 1:
            logger.error('target %s specifies multiple base targets, but only one is allowed', self.getName())
        return None